import streamlit as st

def init_income_inputs():
    if "user_inputs" not in st.session_state:
        st.session_state.user_inputs = {
            "user_annual_income": 50000,
            "partner_annual_income": 50000,
        }

def show_income_inputs():
    st.sidebar.header("Income Information")
    st.session_state.user_inputs["user_annual_income"] = st.sidebar.number_input(
        "Your Annual Income",
        min_value=0,
        value=st.session_state.user_inputs["user_annual_income"],
    )
    st.session_state.user_inputs["partner_annual_income"] = st.sidebar.number_input(
        "Partner's Annual Income",
        min_value=0,
        value=st.session_state.user_inputs["partner_annual_income"],
    )