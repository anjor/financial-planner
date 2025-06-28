"""Authentication module for the financial planner app."""

import hashlib
from typing import Any

import streamlit as st


def hash_password(password: str) -> str:
    """Simple password hashing for demo purposes."""
    return hashlib.sha256(password.encode()).hexdigest()


def create_user_id(email: str) -> str:
    """Create a consistent user ID from email."""
    return hashlib.md5(email.lower().encode()).hexdigest()


def show_auth_form() -> bool:
    """Show authentication form and handle login/signup."""
    st.title("🔐 Financial Planner Login")

    # Create tabs for login and signup
    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    with login_tab:
        with st.form("login_form"):
            st.subheader("Login to Your Account")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            login_submitted = st.form_submit_button("Login")

            if login_submitted:
                if email and password:
                    # For demo purposes, we'll use a simple authentication
                    # In production, you'd use Supabase Auth
                    user_id = create_user_id(email)

                    # Store user info in session state
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.session_state.user_id = user_id

                    st.success("✅ Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Please enter both email and password")

    with signup_tab:
        with st.form("signup_form"):
            st.subheader("Create New Account")
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
            signup_submitted = st.form_submit_button("Sign Up")

            if signup_submitted:
                if new_email and new_password and confirm_password:
                    if new_password == confirm_password:
                        # Create account (simplified for demo)
                        user_id = create_user_id(new_email)

                        # Store user info in session state
                        st.session_state.authenticated = True
                        st.session_state.user_email = new_email
                        st.session_state.user_id = user_id

                        st.success("✅ Account created and logged in!")
                        st.rerun()
                    else:
                        st.error("Passwords don't match")
                else:
                    st.error("Please fill in all fields")

    return False


def logout() -> None:
    """Log out the current user."""
    st.session_state.authenticated = False
    st.session_state.user_email = None
    st.session_state.user_id = None
    st.rerun()


def require_auth() -> bool:
    """Check if user is authenticated, show login form if not."""
    if not st.session_state.get("authenticated", False):
        show_auth_form()
        return False
    return True


def get_current_user() -> dict[str, Any] | None:
    """Get the current authenticated user info."""
    if st.session_state.get("authenticated", False):
        return {
            "email": st.session_state.get("user_email"),
            "user_id": st.session_state.get("user_id")
        }
    return None


def show_user_info() -> None:
    """Show current user info in sidebar."""
    user = get_current_user()
    if user:
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**Logged in as:** {user['email']}")
        if st.sidebar.button("Logout"):
            logout()
