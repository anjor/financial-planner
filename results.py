from projection import calculate_projection


import pandas as pd
import plotly.express as px
import streamlit as st


def show_results_page():
    st.title("UK Financial Planning Tool - Results")

    if "user_inputs" not in st.session_state:
        st.warning("Please enter your financial information on the Input page first.")
        return

    inputs = st.session_state.user_inputs

    # Calculate combined figures
    total_annual_income = inputs["user_annual_income"] + inputs["partner_annual_income"]
    total_net_worth = inputs["user_net_worth"] + inputs["partner_net_worth"]
    total_annual_expenses = (
        inputs["user_annual_expenses"] + inputs["partner_annual_expenses"]
    )

    years_to_project = inputs["life_expectancy"] - inputs["current_age"]

    # Calculate projection
    projection = calculate_projection(
        total_net_worth,
        total_annual_income,
        total_annual_expenses,
        inputs["growth_rate"],
        inputs["inflation_rate"],
        years_to_project,
        inputs["retirement_age"],
        inputs["current_age"],
    )

    # Create DataFrame for plotting
    df = pd.DataFrame(
        {
            "Year": range(inputs["current_age"], inputs["life_expectancy"] + 1),
            "Net Worth": projection,
        }
    )

    # Plot
    fig = px.line(
        df, x="Year", y="Net Worth", title="Projected Combined Net Worth Over Lifetime"
    )
    fig.update_layout(yaxis_title="Net Worth (£)")
    fig.add_vline(
        x=inputs["retirement_age"],
        line_dash="dash",
        line_color="red",
        annotation_text="Retirement Age",
        annotation_position="top right",
    )
    st.plotly_chart(fig)

    # Display some key metrics
    retirement_net_worth = projection[inputs["retirement_age"] - inputs["current_age"]]
    final_net_worth = projection[-1]

    st.write(
        f"Projected Combined Net Worth at Retirement (Age {inputs['retirement_age']}): £{retirement_net_worth:,.2f}"
    )
    st.write(
        f"Projected Combined Net Worth at Life Expectancy (Age {inputs['life_expectancy']}): £{final_net_worth:,.2f}"
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
