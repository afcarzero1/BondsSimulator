from businesses.work import Work, Living
from businesses.activity import Activity
from businesses.banking.bank import BankCD, BankSavings

import pandas as pd


def simulate(simulation_length, salary, expenses, annual_interest_rate):
    all_activities = [
        Work(salary=salary),
        Living(expenses=expenses),
    ]

    savings_account = BankSavings(amount=10_000)

    cds = [
        BankCD(
            number_periods=6, value=3_000, annual_interest_rate=annual_interest_rate
        ),
        BankCD(
            number_periods=7, value=3_000, annual_interest_rate=annual_interest_rate
        ),
        BankCD(
            number_periods=8, value=3_000, annual_interest_rate=annual_interest_rate
        ),
    ]
    all_activities.extend(cds)

    # print("\tBank Account \t Profits \t Equity")
    equities = []
    profits_list = []
    for i in range(simulation_length):
        savings_account, all_activities, profits = monthly_strategy(
            savings_account,
            activities=all_activities,
            annual_interest_rate=annual_interest_rate,
        )

        equity_activities = sum(activity.valuation() for activity in all_activities)
        saving_valuation = savings_account.valuation()

        equity = saving_valuation + equity_activities
        # print(f"{i}\t{saving_valuation:.2f}\t\t{profits:.2f}\t\t{equity:.2f}")
        equities.append(equity)
        profits_list.append(profits)

    return equities, profits_list


def monthly_strategy(
    savings: BankSavings, activities: list[Activity], annual_interest_rate: float
) -> tuple[BankSavings, list[Activity], float]:
    for activity in activities:
        activity.step()

    profits_total = sum(activity.profit() for activity in activities)
    liquid_assets = profits_total + savings.valuation()

    amount_per_cd = 1_000
    minimum_liquid = 6_000

    if liquid_assets <= minimum_liquid + amount_per_cd:
        savings.step(extraction=-profits_total)
    else:
        total_to_invest = liquid_assets - minimum_liquid

        # Extract money from the bank account
        savings.step(extraction=-(profits_total - total_to_invest))

        new_cd = BankCD(
            number_periods=6,
            value=total_to_invest,
            annual_interest_rate=annual_interest_rate,
        )
        activities.append(new_cd)

    return savings, activities, profits_total


if __name__ == "__main__":
    simulate()
