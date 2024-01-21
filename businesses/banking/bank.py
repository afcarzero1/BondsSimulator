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
            loan_value: The initial amount of the loan
            annual_interest_rate:
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
