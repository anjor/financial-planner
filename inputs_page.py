import streamlit as st
from account import Account
from inputs.income import init_income_inputs, show_income_inputs
from inputs.assets import init_assets_inputs, show_assets_inputs

def init_session_state():
    init_income_inputs()
    init_assets_inputs()
    if "user_inputs" not in st.session_state:
        st.session_state.user_inputs.update({
            "user_annual_expenses": 20000,
            "partner_annual_expenses": 20000,
            "current_age": 30,
            "retirement_age": 65,
            "life_expectancy": 85,
            "partner_current_age": 30,
            "partner_retirement_age": 65,
            "partner_life_expectancy": 85,
            "inflation_rate": 0.02,
            "has_partner": False,
        })
    if "user_accounts" not in st.session_state:
        st.session_state.user_accounts = []
    if "partner_accounts" not in st.session_state:
        st.session_state.partner_accounts = []

def show_net_worth_breakdown(prefix):
    return show_assets_inputs(prefix)

def show_input_page():
    st.title("UK Financial Planning Tool")

    # Sidebar for inputs
    st.sidebar.header("Personal Information")
    has_partner = st.sidebar.checkbox("Do you have a partner?")

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
        min_value=st.session_state.user_inputs["retirement_age"],
        max_value=120,
        value=st.session_state.user_inputs["life_expectancy"],
    )

    if has_partner:
        st.session_state.user_inputs["partner_current_age"] = st.sidebar.number_input(
            "Partner's Current Age",
            min_value=18,
            max_value=100,
            value=st.session_state.user_inputs["partner_current_age"],
        )
        st.session_state.user_inputs["partner_retirement_age"] = st.sidebar.number_input(
            "Partner's Retirement Age",
            min_value=st.session_state.user_inputs["partner_current_age"] + 1,
            max_value=100,
            value=st.session_state.user_inputs["partner_retirement_age"],
        )
        st.session_state.user_inputs["partner_life_expectancy"] = st.sidebar.number_input(
            "Partner's Life Expectancy",
            min_value=st.session_state.user_inputs["partner_retirement_age"],
            max_value=120,
            value=st.session_state.user_inputs["partner_life_expectancy"],
        )

    show_income_inputs()
from account import Account


def init_session_state():
    if "user_inputs" not in st.session_state:
        st.session_state.user_inputs = {
            "user_annual_income": 50000,
            "user_annual_expenses": 20000,
            "partner_annual_income": 50000,
            "partner_annual_expenses": 20000,
            "current_age": 30,
            "retirement_age": 65,
            "life_expectancy": 85,
            "partner_current_age": 30,
            "partner_retirement_age": 65,
            "partner_life_expectancy": 85,
            "inflation_rate": 0.02,
            "has_partner": False,
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

    # Sidebar for inputs
    st.sidebar.header("Personal Information")
    has_partner = st.sidebar.checkbox("Do you have a partner?")

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

    if has_partner:
        st.session_state.user_inputs["partner_current_age"] = st.sidebar.number_input(
            "Partner Current Age",
            min_value=18,
            max_value=100,
            value=st.session_state.user_inputs["partner_current_age"],
        )
        st.session_state.user_inputs["partner_retirement_age"] = (
            st.sidebar.number_input(
                "Partner Retirement Age",
                min_value=st.session_state.user_inputs["partner_current_age"] + 1,
                max_value=100,
                value=st.session_state.user_inputs["partner_retirement_age"],
            )
        )
        st.session_state.user_inputs["partner_life_expectancy"] = (
            st.sidebar.number_input(
                "Partner Life Expectancy",
                min_value=st.session_state.user_inputs["partner_retirement_age"] + 1,
                max_value=120,
                value=st.session_state.user_inputs["partner_life_expectancy"],
            )
        )

    # Sidebar for Investment Assumptions
    st.sidebar.header("Investment Assumptions")

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

    st.subheader("You")
    user_annual_income = st.number_input(
        "Post-tax Annual Income (£)",
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

    if has_partner:
        st.subheader("Your Partner")
        partner_annual_income = st.number_input(
            "Post-tax Annual Income (£)",
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
    else:
        partner_annual_income = 0
        partner_annual_expenses = 0
        partner_net_worth = 0
        partner_net_worth_breakdown = {}

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
            "has_partner": has_partner,
        }
    )
