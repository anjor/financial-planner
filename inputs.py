import streamlit as st


def show_net_worth_breakdown(prefix):
    categories = {
        "Cash": 0.01,  # Low growth rate for cash
        "Stocks": 0.07,  # Higher growth rate for stocks
        "Bonds": 0.03,  # Moderate growth rate for bonds
        "Real Estate": 0.04,  # Moderate growth rate for real estate
        "Pension": 0.05,  # Moderate growth rate for pension
        "Other": 0.02,  # Low growth rate for other assets
    }

    total = 0
    breakdown = {}

    st.subheader("Net Worth Breakdown")
    for category, default_growth in categories.items():
        col1, col2 = st.columns(2)
        with col1:
            value = st.number_input(
                f"{category} (£)", min_value=0, value=0, key=f"{prefix}_{category}"
            )
        with col2:
            growth = (
                st.number_input(
                    f"{category} Growth Rate (%)",
                    min_value=0.0,
                    max_value=20.0,
                    value=default_growth * 100,
                    key=f"{prefix}_{category}_growth",
                )
                / 100
            )
        total += value
        breakdown[category] = {"value": value, "growth": growth}

    return total, breakdown


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
        user_annual_expenses = st.number_input(
            "Annual Expenses (£)", min_value=0, value=40000, key="user_expenses"
        )
        user_net_worth, user_net_worth_breakdown = show_net_worth_breakdown("user")

    with col2:
        st.subheader("Your Partner")
        partner_annual_income = st.number_input(
            "Annual Income (£)", min_value=0, value=50000, key="partner_income"
        )
        partner_annual_expenses = st.number_input(
            "Annual Expenses (£)", min_value=0, value=40000, key="partner_expenses"
        )
        partner_net_worth, partner_net_worth_breakdown = show_net_worth_breakdown(
            "partner"
        )

    st.header("Investment Assumptions")

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
        "user_net_worth_breakdown": user_net_worth_breakdown,
        "user_annual_expenses": user_annual_expenses,
        "partner_annual_income": partner_annual_income,
        "partner_net_worth": partner_net_worth,
        "partner_net_worth_breakdown": partner_net_worth_breakdown,
        "partner_annual_expenses": partner_annual_expenses,
        "current_age": current_age,
        "retirement_age": retirement_age,
        "life_expectancy": life_expectancy,
        "inflation_rate": inflation_rate,
    }
