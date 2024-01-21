import streamlit as st
import matplotlib.pyplot as plt
from main import simulate

# Define your other necessary classes and functions

st.title("Financial Simulation App")

# Getting user inputs
salary = st.number_input("Enter your monthly salary:", min_value=500, value=3000)
expenses = st.number_input(
    "Enter your monthly living expenses:", min_value=500, value=2000
)
annual_interest_rate = st.slider(
    "Select the annual interest rate for Bank CD:", 0.0, 1.0, value=0.15
)

simulation_length = st.slider(
    "Select the length of simulation (years)", min_value=1, max_value=30, value=5
)  # Or make this a user input
simulation_length = simulation_length * 12

# Running the simulation
equities, profits = simulate(simulation_length, salary, expenses, annual_interest_rate)

# Calculate baseline savings
baseline_savings = [(salary - expenses) * month + 19_000 for month in range(simulation_length)]


# Plotting the results
fig, ax = plt.subplots()
ax.plot(equities, label="Equity")
ax.plot(profits, label="Profits")
ax.plot(baseline_savings, label="Baseline Savings", linestyle='--')
ax.set_xlabel("Months")
ax.set_ylabel("Amount")
ax.set_title("Financial Simulation Results")
ax.legend()
# Displaying metrics
# Calculate final values and difference
final_equity = equities[-1] if equities else 0
final_baseline = baseline_savings[-1] if baseline_savings else 0
difference = final_equity - final_baseline

cols = st.columns(3)
with cols[0]:
    st.metric(label="Final Equity", value=f"${final_equity:,.2f}")
with cols[1]:
    st.metric(label="Final Baseline Savings", value=f"${final_baseline:,.2f}")
with cols[2]:
    st.metric(label="Difference", value=f"${difference:,.2f}")
st.pyplot(fig)
