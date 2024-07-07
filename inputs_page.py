import streamlit as st
from account import Account
from inputs.income import init_income_inputs, show_income_inputs
from inputs.assets import init_assets_inputs, show_assets_inputs


def init_session_state():
    init_income_inputs()
    init_assets_inputs()
    if "user_inputs" not in st.session_state:
        st.session_state.user_inputs = {
            "inflation_rate": 0.02,
            "has_partner": False,
        }
    if "age_inputs" not in st.session_state:
        st.session_state.age_inputs = {
            "current_age": 30,
            "retirement_age": 65,
            "life_expectancy": 85,
            "partner_current_age": 30,
            "partner_retirement_age": 65,
            "partner_life_expectancy": 85,
        }
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

    st.session_state.age_inputs["current_age"] = st.sidebar.number_input(
        "Current Age",
        min_value=18,
        max_value=100,
        value=st.session_state.age_inputs["current_age"],
    )
    st.session_state.age_inputs["retirement_age"] = st.sidebar.number_input(
        "Retirement Age",
        min_value=st.session_state.age_inputs["current_age"] + 1,
        max_value=100,
        value=st.session_state.age_inputs["retirement_age"],
    )
    st.session_state.age_inputs["life_expectancy"] = st.sidebar.number_input(
        "Life Expectancy",
        min_value=st.session_state.age_inputs["retirement_age"],
        max_value=120,
        value=st.session_state.age_inputs["life_expectancy"],
    )

    if has_partner:
        st.session_state.age_inputs["partner_current_age"] = st.sidebar.number_input(
            "Partner's Current Age",
            min_value=18,
            max_value=100,
            value=st.session_state.age_inputs["partner_current_age"],
        )
        st.session_state.age_inputs["partner_retirement_age"] = st.sidebar.number_input(
            "Partner's Retirement Age",
            min_value=st.session_state.age_inputs["partner_current_age"] + 1,
            max_value=100,
            value=st.session_state.age_inputs["partner_retirement_age"],
        )
        st.session_state.age_inputs["partner_life_expectancy"] = (
            st.sidebar.number_input(
                "Partner's Life Expectancy",
                min_value=st.session_state.age_inputs["partner_retirement_age"],
                max_value=120,
                value=st.session_state.age_inputs["partner_life_expectancy"],
            )
        )

    show_income_inputs()
    show_assets_inputs("user")
    if has_partner:
        show_assets_inputs("partner")
