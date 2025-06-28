import streamlit as st

from auth import require_auth, show_user_info
from inputs_page import show_input_page
from results import show_results_page
from scenario_manager import show_scenario_selector
from state import init_state


def main() -> None:
    st.set_page_config(
        page_title="UK Financial Planning Tool", page_icon="£", layout="wide"
    )

    # Initialize session state
    init_state()

    # Check authentication first
    if not require_auth():
        return

    # Show user info in sidebar
    show_user_info()

    # Show scenario quick loader
    show_scenario_selector()

    # Create a sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Input", "Results", "Scenarios"])

    # Show the selected page
    if page == "Input":
        show_input_page()
    elif page == "Results":
        show_results_page()
    elif page == "Scenarios":
        from scenario_manager import show_scenario_manager
        show_scenario_manager()


if __name__ == "__main__":
    main()
