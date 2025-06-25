import streamlit as st

from account import Account, HoldingsType


def show_assets_inputs(prefix: str) -> None:
    total = 0
    breakdown = {}

    st.subheader("Net Worth Breakdown")

    # Display existing accounts
    for i, account in enumerate(st.session_state[f"{prefix}_accounts"]):
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
        with col1:
            account.name = st.text_input(
                "Account Name", value=account.name, key=f"{prefix}_name_{i}"
            )
        with col2:
            account.value = st.number_input(
                "Value (£)",
                min_value=0,
                value=account.value,
                key=f"{prefix}_value_{i}",
            )
        with col3:
            account.growth_rate =  st.number_input(
                    "Growth Rate (%)",
                    min_value=0.0,
                    max_value=20.0,
                    value=account.growth_rate * 100,
                    key=f"{prefix}_growth_{i}",
                ) or 0
            account.growth_rate /= 100
        with col4:
            selected_type = st.selectbox(
                "Holdings Type",
                options=[ht.name for ht in HoldingsType],
                index=[ht.name for ht in HoldingsType].index(account.holdings_type.name),
                key=f"{prefix}_type_{i}"
            )
            account.holdings_type = HoldingsType[selected_type]
        with col5:
            if st.button("Remove", key=f"{prefix}_remove_{i}"):
                st.session_state[f"{prefix}_accounts"].pop(i)
                st.rerun()

        total += account.value or 0
        breakdown[account.name] = {
            "value": account.value,
            "growth": account.growth_rate,
            "is_liquid": account.is_liquid,
        }

    # Add new account button
    if st.button(f"Add New {prefix.capitalize()} Account"):
        new_account = Account(
            name=f"New Account {len(st.session_state[f'{prefix}_accounts'])+1}",
            holdings_type=HoldingsType.CASH,
            growth_rate=.02,
        )
        st.session_state[f"{prefix}_accounts"].append(new_account)
        st.rerun()

    st.session_state.user_inputs[f"{prefix}_net_worth"] = total
    st.session_state.user_inputs[f"{prefix}_net_worth_breakdown"] = breakdown
