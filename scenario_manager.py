"""Scenario management for saving and loading financial plans."""

from datetime import datetime
from typing import Any

import streamlit as st

from auth import get_current_user
from database import get_db_manager


def get_session_state_data() -> dict[str, Any]:
    """Extract all relevant session state data for saving."""
    return {
        "user_inputs": st.session_state.get("user_inputs", {}),
        "age_inputs": st.session_state.get("age_inputs", {}),
        "user_accounts": [
            {
                "name": acc.name,
                "holdings_type": acc.holdings_type.value,
                "value": acc.value,
                "growth_rate": acc.growth_rate
            }
            for acc in st.session_state.get("user_accounts", [])
        ],
        "partner_accounts": [
            {
                "name": acc.name,
                "holdings_type": acc.holdings_type.value,
                "value": acc.value,
                "growth_rate": acc.growth_rate
            }
            for acc in st.session_state.get("partner_accounts", [])
        ],
        "saved_at": datetime.now().isoformat()
    }


def load_session_state_data(data: dict[str, Any]) -> None:
    """Load data back into session state."""
    from account import Account, HoldingsType

    if "user_inputs" in data:
        st.session_state.user_inputs = data["user_inputs"]

    if "age_inputs" in data:
        st.session_state.age_inputs = data["age_inputs"]

    if "user_accounts" in data:
        st.session_state.user_accounts = [
            Account(
                name=acc["name"],
                holdings_type=HoldingsType(acc["holdings_type"]),
                value=acc["value"],
                growth_rate=acc["growth_rate"]
            )
            for acc in data["user_accounts"]
        ]

    if "partner_accounts" in data:
        st.session_state.partner_accounts = [
            Account(
                name=acc["name"],
                holdings_type=HoldingsType(acc["holdings_type"]),
                value=acc["value"],
                growth_rate=acc["growth_rate"]
            )
            for acc in data["partner_accounts"]
        ]


def show_scenario_manager() -> None:
    """Show the scenario management interface."""
    user = get_current_user()
    if not user:
        st.error("You must be logged in to manage scenarios")
        return

    st.subheader("💾 Scenario Management")

    db = get_db_manager()

    # Save current scenario
    col1, col2 = st.columns([2, 1])

    with col1:
        scenario_name = st.text_input("Scenario Name", placeholder="e.g., Conservative Plan, Aggressive Growth")

    with col2:
        if st.button("Save Current Scenario", type="primary"):
            if scenario_name:
                scenario_data = get_session_state_data()
                success = db.save_user_scenario(user["user_id"], scenario_name, scenario_data)
                if success:
                    st.success(f"✅ Scenario '{scenario_name}' saved!")
                    st.rerun()
                else:
                    st.error("Failed to save scenario")
            else:
                st.error("Please enter a scenario name")

    st.markdown("---")

    # Load existing scenarios
    st.subheader("📂 Your Saved Scenarios")

    scenarios = db.list_user_scenarios(user["user_id"])

    if not scenarios:
        st.info("No saved scenarios yet. Save your current inputs above to get started!")
        return

    for scenario in scenarios:
        col1, col2, col3, col4 = st.columns([3, 2, 1, 1])

        with col1:
            st.write(f"**{scenario['scenario_name']}**")

        with col2:
            updated_at = datetime.fromisoformat(scenario['updated_at'].replace('Z', '+00:00'))
            st.write(f"Updated: {updated_at.strftime('%Y-%m-%d %H:%M')}")

        with col3:
            if st.button("Load", key=f"load_{scenario['scenario_name']}"):
                scenario_data = db.load_user_scenario(user["user_id"], scenario['scenario_name'])
                if scenario_data:
                    load_session_state_data(scenario_data)
                    st.success(f"✅ Loaded '{scenario['scenario_name']}'")
                    st.rerun()
                else:
                    st.error("Failed to load scenario")

        with col4:
            if st.button("Delete", key=f"delete_{scenario['scenario_name']}", type="secondary"):
                success = db.delete_user_scenario(user["user_id"], scenario['scenario_name'])
                if success:
                    st.success(f"🗑️ Deleted '{scenario['scenario_name']}'")
                    st.rerun()
                else:
                    st.error("Failed to delete scenario")


def show_scenario_selector() -> None:
    """Show a compact scenario selector for the sidebar."""
    user = get_current_user()
    if not user:
        return

    db = get_db_manager()
    scenarios = db.list_user_scenarios(user["user_id"])

    if scenarios:
        st.sidebar.markdown("---")
        st.sidebar.subheader("💾 Quick Load")

        scenario_names = [s["scenario_name"] for s in scenarios]
        selected = st.sidebar.selectbox("Load Scenario", [""] + scenario_names, key="quick_load_scenario")

        if selected:
            scenario_data = db.load_user_scenario(user["user_id"], selected)
            if scenario_data:
                load_session_state_data(scenario_data)
                st.sidebar.success(f"✅ Loaded '{selected}'")
                st.rerun()
