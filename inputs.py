import streamlit as st


def show_input_page():
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
            "Expected Annual Inflation Rate (%)",
            min_value=0.0,
            max_value=10.0,
            value=2.0,
        )
        / 100
    )

    # Store the input values in session state
    st.session_state.user_inputs = {
        "user_annual_income": user_annual_income,
        "user_net_worth": user_net_worth,
        "user_annual_expenses": user_annual_expenses,
        "partner_annual_income": partner_annual_income,
        "partner_net_worth": partner_net_worth,
        "partner_annual_expenses": partner_annual_expenses,
        "growth_rate": growth_rate,
        "current_age": current_age,
        "retirement_age": retirement_age,
        "life_expectancy": life_expectancy,
        "inflation_rate": inflation_rate,
    }
