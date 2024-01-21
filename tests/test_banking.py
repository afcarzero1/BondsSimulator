import math
import unittest
from businesses import BankLoan


def calculate_new_payment(remaining_principal, annual_interest_rate, remaining_periods):
    """
    Calculate the new monthly payment for a loan given a change in interest rate.

    Args:
        remaining_principal (float): The remaining principal of the loan.
        annual_interest_rate (float): The new annual interest rate (as a decimal).
        remaining_periods (int): The remaining number of periods (months) of the loan.

    Returns:
        float: The new monthly payment amount.
    """
    if annual_interest_rate == 0:
        return remaining_principal / remaining_periods

    monthly_interest_rate = annual_interest_rate / 12
    payment = remaining_principal * (
        monthly_interest_rate
        / (1 - math.pow(1 + monthly_interest_rate, -remaining_periods))
    )
    return payment


class TestLoan(unittest.TestCase):
    def test_fixed_rate(self):
        total_duration = 30 * 12
        interest_rate = 5.5 / 100
        loan_value = 375_000

        loan = BankLoan(
            loan_value=loan_value,
            annual_interest_rate=interest_rate,
            loan_duration=total_duration,
        )

        self.assertAlmostEqual(loan.monthly_payment, 2_129.208755, places=5)
        self.assertEqual(loan.valuation(), -loan_value)
        self.assertRaises(ValueError, loan.profit)

        for _ in range(total_duration):
            loan.step(payment=loan.monthly_payment)

            self.assertAlmostEqual(loan.profit(), -2_129.208755, places=5)

        self.assertAlmostEqual(loan.valuation(), 0, places=5)

    def test_variable_rate_simple(self):
        total_duration = 30 * 12
        interest_rate = 5.5 / 100
        loan_value = 375_000

        new_interest_rate = 6.5 / 100

        loan = BankLoan(
            loan_value=loan_value,
            annual_interest_rate=interest_rate,
            loan_duration=total_duration,
        )

        self.assertAlmostEqual(loan.monthly_payment, 2_129.208755, places=5)
        self.assertEqual(loan.valuation(), -loan_value)
        self.assertRaises(ValueError, loan.profit)

        for i in range(total_duration):
            if i == 0:
                loan.step(payment=2370.25508809862, new_interest_rate=new_interest_rate)
                self.assertAlmostEqual(loan.profit(), -2370.255088, places=5)
            else:
                loan.step(payment=2370.25508809862)

        self.assertAlmostEqual(loan.valuation(), 0, places=5)

    def no_test_variable_rate_complex(self):
        total_duration = 30 * 12  # 30 years
        initial_interest_rate = 4.5 / 100  # 4.5%
        loan_value = 300_000  # Loan amount

        loan = BankLoan(
            loan_value=loan_value,
            annual_interest_rate=initial_interest_rate,
            loan_duration=total_duration,
        )

        # Simulate interest rate changes at different periods
        rate_changes = {
            12 * 5: 5.0 / 100,  # 5% after 5 years
            12 * 10: 4.0 / 100,  # 4% after 10 years
            12 * 15: 6.0 / 100,  # 6% after 15 years
        }

        for month in range(total_duration):
            remaining_periods = total_duration - month
            new_rate = rate_changes.get(month)
            if new_rate:
                new_payment = calculate_new_payment(
                    loan.remaining_principal, new_rate, remaining_periods
                )
                loan.step(payment=new_payment, new_interest_rate=new_rate)
                # Assert the profit and valuation at the point of rate change
                self.assertAlmostEqual(loan.profit(), -new_payment, places=2)
                self.assertLess(
                    loan.valuation(), 0
                )  # Valuation should be less than 0 (liability)
            else:
                loan.step(payment=loan.monthly_payment)

        # Final assertions
        self.assertAlmostEqual(loan.valuation(), 0, places=2)
