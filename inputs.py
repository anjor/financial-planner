import streamlit as st
from account import Account


def init_session_state():
    if "user_inputs" not in st.session_state:
        st.session_state.user_inputs = {
            "user_annual_income": 50000,
            "user_annual_expenses": 40000,
            "partner_annual_income": 50000,
            "partner_annual_expenses": 40000,
            "current_age": 30,
            "retirement_age": 65,
            "life_expectancy": 85,
            "inflation_rate": 0.02,
        }
    if "user_accounts" not in st.session_state:
        st.session_state.user_accounts = []
    if "partner_accounts" not in st.session_state:
        st.session_state.partner_accounts = []


def show_net_worth_breakdown(prefix):
    if f"{prefix}_accounts" not in st.session_state:
        st.session_state[f"{prefix}_accounts"] = []
    total = 0
    breakdown = {}

    st.subheader("Net Worth Breakdown")

    # Display existing accounts
    for i, account in enumerate(st.session_state[f"{prefix}_accounts"]):
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        with col1:
            account.name = st.text_input(
                f"Account Name", value=account.name, key=f"{prefix}_name_{i}"
            )
        with col2:
            account.value = st.number_input(
                f"Value (£)",
                min_value=0,
                value=account.value,
                key=f"{prefix}_value_{i}",
            )
        with col3:
            account.growth_rate = (
                st.number_input(
                    f"Growth Rate (%)",
                    min_value=0.0,
                    max_value=20.0,
                    value=account.growth_rate * 100,
                    key=f"{prefix}_growth_{i}",
                )
                / 100
            )
        with col4:
            if st.button("Remove", key=f"{prefix}_remove_{i}"):
                st.session_state[f"{prefix}_accounts"].pop(i)
                st.experimental_rerun()

        total += account.value
        breakdown[account.name] = {
            "value": account.value,
            "growth": account.growth_rate,
        }

    # Add new account button
    if st.button(f"Add New {prefix.capitalize()} Account"):
        new_account = Account(
            f"New Account {len(st.session_state[f'{prefix}_accounts'])+1}",
            "Other",
            0.02,
        )
        st.session_state[f"{prefix}_accounts"].append(new_account)
        st.experimental_rerun()
    return total, breakdown


def show_input_page():
    st.title("UK Financial Planning Tool")

    # Sidebar for Investment Assumptions
    st.sidebar.header("Investment Assumptions")

    st.session_state.user_inputs["current_age"] = st.sidebar.number_input(
        "Current Age",
        min_value=18,
        max_value=100,
        value=st.session_state.user_inputs["current_age"],
    )
    st.session_state.user_inputs["retirement_age"] = st.sidebar.number_input(
        "Retirement Age",
        min_value=st.session_state.user_inputs["current_age"] + 1,
        max_value=100,
        value=st.session_state.user_inputs["retirement_age"],
    )
    st.session_state.user_inputs["life_expectancy"] = st.sidebar.number_input(
        "Life Expectancy",
        min_value=st.session_state.user_inputs["retirement_age"] + 1,
        max_value=120,
        value=st.session_state.user_inputs["life_expectancy"],
    )
    st.session_state.user_inputs["inflation_rate"] = (
        st.sidebar.number_input(
            "Expected Annual Inflation Rate (%)",
            min_value=0.0,
            max_value=10.0,
            value=st.session_state.user_inputs["inflation_rate"] * 100,
        )
        / 100
    )

    # Main content
    st.header("Enter Your Financial Information")

    # Create two columns for User and Partner inputs
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("You")
        user_annual_income = st.number_input(
            "Annual Income (£)",
            min_value=0,
            value=st.session_state.user_inputs["user_annual_income"],
            key="user_income",
        )
        user_annual_expenses = st.number_input(
            "Annual Expenses (£)",
            min_value=0,
            value=st.session_state.user_inputs["user_annual_expenses"],
            key="user_expenses",
        )
        user_net_worth, user_net_worth_breakdown = show_net_worth_breakdown("user")

    with col2:
        st.subheader("Your Partner")
        partner_annual_income = st.number_input(
            "Annual Income (£)",
            min_value=0,
            value=st.session_state.user_inputs["partner_annual_income"],
            key="partner_income",
        )
        partner_annual_expenses = st.number_input(
            "Annual Expenses (£)",
            min_value=0,
            value=st.session_state.user_inputs["partner_annual_expenses"],
            key="partner_expenses",
        )
        partner_net_worth, partner_net_worth_breakdown = show_net_worth_breakdown(
            "partner"
        )

    # Update the session state with the latest values
    st.session_state.user_inputs.update(
        {
            "user_annual_income": user_annual_income,
            "user_annual_expenses": user_annual_expenses,
            "partner_annual_income": partner_annual_income,
            "partner_annual_expenses": partner_annual_expenses,
            "user_net_worth": user_net_worth,
            "user_net_worth_breakdown": user_net_worth_breakdown,
            "partner_net_worth": partner_net_worth,
            "partner_net_worth_breakdown": partner_net_worth_breakdown,
        }
    )
