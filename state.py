import streamlit as st


def init_state():
    # income and expenses
    if "user_inputs" not in st.session_state:
        st.session_state.user_inputs = {
            "user_annual_income": 50000,
            "partner_annual_income": 50000,
            "user_annual_expenses": 20000,
            "partner_annual_expenses": 20000,
            "inflation_rate": 0.02,
            "has_partner": False,
        }

    # assets
    for prefix in ["user", "partner"]:

        if f"{prefix}_accounts" not in st.session_state:
            st.session_state[f"{prefix}_accounts"] = []
        if f"{prefix}_net_worth" not in st.session_state.user_inputs:
            st.session_state.user_inputs[f"{prefix}_net_worth"] = 0
        if f"{prefix}_net_worth_breakdown" not in st.session_state.user_inputs:
            st.session_state.user_inputs[f"{prefix}_net_worth_breakdown"] = {}

    # age
    if "age_inputs" not in st.session_state:
        st.session_state.age_inputs = {
            "current_age": 30,
            "retirement_age": 65,
            "life_expectancy": 85,
            "partner_current_age": 30,
            "partner_retirement_age": 65,
            "partner_life_expectancy": 85,
        }
