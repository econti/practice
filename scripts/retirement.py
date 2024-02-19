from random import sample
from typing import Tuple

# Economic assumptions
ANNUAL_INFLATION_RATE = 0.0325

# Grows w/inflation to keep up with cost of living
STARTING_DOLLARS = 100000
MONTHLY_POST_TAX_DOLLARS_NEEDED = 5100
NUM_WITHDRAW_YEARS = 55
TAX_RATE = 0.25

# Define a portion of monthly dollars that goes towards a mortgage and
# when this expense ends. The mortgage will be treated as exempt from
# inflation and terminating after REMAINING_MORTGAGE_YEARS. Set MORTGAGE_AMOUNT
# to 0 if no morgage.
MORTGAGE_AMOUNT = 5100
REMAINING_MORTGAGE_YEARS = 28

# One time large expenses (e.g. kid's college) in format of
# {key: year, value: amount, ...}. Amount will be inflation adjusted.
ONE_TIME_EXPENSES = {
    17: 250000 / 4,
    18: 250000 / 4,
    19: 250000 / 2,
    20: 250000 / 2,
    21: 250000 / 4,
    22: 250000 / 4,
}

# S&P 500 annual returns [1928 - 2023]
SP_500_RETURNS = [
    1.24,
    0.81,
    1.27,
    1.16,
    1.29,
    0.94,
    1.19,
    1.10,
    0.99,
    1.11,
    1.30,
    1.13,
    1.00,
    1.13,
    1.23,
    0.62,
    1.04,
    1.14,
    1.03,
    1.09,
    1.26,
    0.77,
    0.87,
    0.90,
    1.20,
    1.27,
    1.31,
    1.20,
    1.34,
    0.98,
    1.07,
    1.04,
    1.26,
    0.93,
    1.27,
    1.12,
    1.02,
    1.15,
    1.26,
    1.01,
    1.17,
    1.15,
    0.90,
    1.26,
    1.12,
    1.01,
    0.89,
    1.19,
    1.32,
    0.70,
    0.83,
    1.16,
    1.11,
    1.00,
    0.89,
    1.08,
    1.20,
    0.87,
    1.09,
    1.13,
    1.19,
    0.88,
    1.23,
    0.97,
    1.08,
    1.38,
    0.86,
    1.03,
    1.26,
    1.45,
    0.93,
    1.12,
    1.16,
    1.22,
    1.10,
    0.99,
    1.00,
    0.88,
    1.31,
    1.14,
    1.19,
    1.12,
    0.82,
    0.85,
    0.95,
    1.25,
    0.61,
    1.28,
    1.41,
    0.94,
    1.47,
    0.85,
    0.53,
    0.72,
    0.88,
    1.38,
]


def simulate(trials: int = 3000) -> Tuple[float, float]:
    ending_dollars = []
    for i in range(trials):
        if i % 100 == 0:
            print(f"Trials completed: {i}/{trials}", flush=True, end="...\r")

        year_start_balance = STARTING_DOLLARS

        for year in range(NUM_WITHDRAW_YEARS):
            year_start_balance -= ONE_TIME_EXPENSES.get(year, 0) * (
                (1 + ANNUAL_INFLATION_RATE) ** year
            )
            monthly_dollars_needed = MONTHLY_POST_TAX_DOLLARS_NEEDED

            has_mortgage = MORTGAGE_AMOUNT > 0
            mortgage_paid_off = year + 1 > REMAINING_MORTGAGE_YEARS
            if has_mortgage and mortgage_paid_off:
                monthly_dollars_needed -= MORTGAGE_AMOUNT
                monthly_dollars_needed = monthly_dollars_needed * (
                    (1 + ANNUAL_INFLATION_RATE) ** year
                )
            elif has_mortgage and not mortgage_paid_off:
                inflation_affected_dollars = monthly_dollars_needed - MORTGAGE_AMOUNT
                monthly_dollars_needed = (
                    inflation_affected_dollars * ((1 + ANNUAL_INFLATION_RATE) ** year)
                    + MORTGAGE_AMOUNT
                )

            for _ in range(12):
                monthly_drawdown = monthly_dollars_needed / (1 - TAX_RATE)
                year_start_balance -= monthly_drawdown
                # Draw a random year and convert it to a monthly rate of return
                # This is an approximation to of actual monthly returns of the index
                randomly_monthly_return = sample(SP_500_RETURNS, 1)[0] ** (1 / 12)
                year_start_balance = year_start_balance * randomly_monthly_return

            if year_start_balance <= 0:
                break

        ending_dollars.append(year_start_balance)

    avg_end_amount = sum(ending_dollars) / len(ending_dollars)
    prob_run_out = (
        1 - len([x for x in ending_dollars if x > 0]) / len(ending_dollars)
    ) * 100

    return avg_end_amount, prob_run_out


avg_end_amout, prob_run_out = simulate()

print("-" * 20)
print(f"\nAverage ending amount: ${avg_end_amout:.2f}")
print(
    f"Probability of running out of money before {NUM_WITHDRAW_YEARS} years: {prob_run_out:.2f}%"
)
