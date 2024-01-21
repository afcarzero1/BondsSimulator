from ..activity import Activity
import numpy_financial as npf


class BankLoan(Activity):
    def __init__(
        self,
        loan_value: float,
        annual_interest_rate: float,
        loan_duration: int,
        **kwargs
    ):
        """

        Args:
            loan_value: The initial amount of the loan.
            annual_interest_rate: The annual interest rate of the loan.
            loan_duration: Duration of the loan in months
            **kwargs:
        """
        assert 0 < annual_interest_rate < 1
        super().__init__(**kwargs)
        self.loan_value = loan_value
        self.annual_interest_rate = annual_interest_rate
        self.loan_duration = loan_duration

        self.remaining_principal = self.loan_value

        # Compute the monthly payment here
        self.monthly_payment = self._monthly_payment()

        # Initialize variables
        self._current_valuation = -self.loan_value
        self.interest_payments = []

    def valuation(self) -> float:
        return -self.remaining_principal

    def _step(
        self, payment: float, new_interest_rate: float | None = None
    ) -> tuple[float, float]:
        if new_interest_rate is not None:
            # Recompute monthly payment
            assert 0 < new_interest_rate < 1
            self.annual_interest_rate = new_interest_rate
            self.monthly_payment = self._monthly_payment()

            raise NotImplementedError("Variable interest rate not implemented yet.")
        if payment != self.monthly_payment:
            raise NotImplementedError("Late or overpayments not implemented yet")

        interest_paid = self._interest_payment()
        payment_to_principal = payment - interest_paid

        # Update the principal
        self.remaining_principal -= payment_to_principal

        return -payment, -self.remaining_principal

    def _monthly_payment(self) -> float:
        return abs(
            npf.pmt(
                rate=self.annual_interest_rate / 12,
                pv=self.remaining_principal,
                nper=(self.loan_duration - self.current_period),
                fv=0,
            )
        )

    def _interest_payment(self) -> float:
        """
        Interest amount for a given period

        Returns:

        """
        return (self.annual_interest_rate / 12) * self.remaining_principal

    def reset(self):
        super().reset()
        self.interest_payments = []
        self.remaining_principal = self.loan_value


class BankCD(Activity):
    """
    This is a certificate of deposit to a fixed term.
    """

    def __init__(
        self, number_periods: int, value: float, annual_interest_rate: float, **kwargs
    ):
        super().__init__(**kwargs)

        self.number_periods = number_periods
        self.annual_interest_rate = annual_interest_rate
        self.value = value
        self._current_valuation = self.value

    def _step(self) -> tuple[float, float]:
        # The current period is "delayed"
        if self.current_period < self.number_periods - 1:
            return 0, self.value
        elif self.current_period == self.number_periods - 1:
            return (
                self.value
                + self.value * (self.annual_interest_rate * self.number_periods / 12),
                0,
            )
        else:
            return 0, 0


class BankSavings(Activity):
    def __init__(self, amount: float):
        super().__init__()
        self.amount = amount
        self._current_valuation = amount

    def _step(self, extraction: float) -> tuple[float, float]:
        if extraction > self.amount:
            raise ValueError("Attempted to take more money than available")
        self.amount -= extraction
        return extraction, self.amount
