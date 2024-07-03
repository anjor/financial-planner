import streamlit as st
import pandas as pd
import plotly.express as px


def calculate_projection(
    initial_net_worth,
    annual_income,
    annual_expenses,
    inflation_rate,
    growth_rate,
    years,
    retirement_age,
    current_age,
):
    net_worth = [initial_net_worth]
    for year in range(1, years + 1):
        # Adjust income and expenses for inflation
        inflated_income = annual_income * (1 + inflation_rate) ** year
        inflated_expenses = annual_expenses * (1 + inflation_rate) ** year
        if current_age + year <= retirement_age:
            annual_savings = inflated_income - inflated_expenses
        else:
            annual_savings = (
                -inflated_expenses
            )  # In retirement, we're drawing down savings

            # Use real growth rate (nominal growth rate - inflation rate)
        real_growth_rate = (1 + growth_rate) / (1 + inflation_rate) - 1
        new_worth = net_worth[-1] * (1 + real_growth_rate) + annual_savings
        net_worth.append(max(0, new_worth))  # Ensure net worth doesn't go negative
    return net_worth


st.title("UK Financial Planning Tool")

st.header("Enter Your Financial Information")

# Create two columns for User and Partner inputs
col1, col2 = st.columns(2)

with col1:
    st.subheader("You")
    user_annual_income = st.number_input(
        "Annual Income (£)", min_value=0, value=50000, key="user_income"
    )
    user_net_worth = st.number_input(
        "Current Net Worth (£)", min_value=0, value=100000, key="user_net_worth"
    )
    user_annual_expenses = st.number_input(
        "Annual Expenses (£)", min_value=0, value=40000, key="user_expenses"
    )

with col2:
    st.subheader("Your Partner")
    partner_annual_income = st.number_input(
        "Annual Income (£)", min_value=0, value=50000, key="partner_income"
    )
    partner_net_worth = st.number_input(
        "Current Net Worth (£)", min_value=0, value=100000, key="partner_net_worth"
    )
    partner_annual_expenses = st.number_input(
        "Annual Expenses (£)", min_value=0, value=40000, key="partner_expenses"
    )

st.header("Investment Assumptions")

growth_rate = (
    st.slider(
        "Expected Annual Growth Rate (%)", min_value=0.0, max_value=15.0, value=7.0
    )
    / 100
)
current_age = st.slider("Current Age", min_value=18, max_value=100, value=30)
retirement_age = st.slider(
    "Retirement Age", min_value=current_age + 1, max_value=100, value=65
)
life_expectancy = st.slider(
    "Life Expectancy", min_value=retirement_age + 1, max_value=120, value=85
)
inflation_rate = (
    st.slider(
        "Expected Annual Inflation Rate (%)", min_value=0.0, max_value=10.0, value=2.0
    )
    / 100
)


years_to_project = life_expectancy - current_age

# Calculate combined figures
total_annual_income = user_annual_income + partner_annual_income
total_net_worth = user_net_worth + partner_net_worth
total_annual_expenses = user_annual_expenses + partner_annual_expenses

# Calculate projection
projection = calculate_projection(
    total_net_worth,
    total_annual_income,
    total_annual_expenses,
    growth_rate,
    inflation_rate,
    years_to_project,
    retirement_age,
    current_age,
)

# Create DataFrame for plotting
df = pd.DataFrame(
    {"Year": range(current_age, life_expectancy + 1), "Net Worth": projection}
)

# Plot
fig = px.line(
    df, x="Year", y="Net Worth", title="Projected Combined Net Worth Over Lifetime"
)
fig.update_layout(yaxis_title="Net Worth (£)")
fig.add_vline(
    x=retirement_age,
    line_dash="dash",
    line_color="red",
    annotation_text="Retirement Age",
    annotation_position="top right",
)
st.plotly_chart(fig)

# Display some key metrics
retirement_net_worth = projection[retirement_age - current_age]
final_net_worth = projection[-1]

st.write(
    f"Projected Combined Net Worth at Retirement (Age {retirement_age}): £{retirement_net_worth:,.2f}"
)
st.write(
    f"Projected Combined Net Worth at Life Expectancy (Age {life_expectancy}): £{final_net_worth:,.2f}"
)

annual_retirement_income = retirement_net_worth * 0.04  # Using the 4% rule
st.write(
    f"Estimated Annual Retirement Income (4% Rule): £{annual_retirement_income:,.2f}"
)

# Display current combined figures
st.header("Current Combined Figures")
st.write(f"Total Annual Income: £{total_annual_income:,.2f}")
st.write(f"Total Current Net Worth: £{total_net_worth:,.2f}")
st.write(f"Total Annual Expenses: £{total_annual_expenses:,.2f}")
