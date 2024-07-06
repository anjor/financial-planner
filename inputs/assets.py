import streamlit as st
from account import Account

def init_assets_inputs():
    if "user_accounts" not in st.session_state:
        st.session_state.user_accounts = []
    if "partner_accounts" not in st.session_state:
        st.session_state.partner_accounts = []

def show_assets_inputs(prefix):
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
