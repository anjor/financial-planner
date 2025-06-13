import streamlit as st
from typing import Dict, Any, Optional


def validate_age_inputs(age_inputs: Dict[str, Any]) -> Optional[str]:
    """Validate age-related inputs and return error message if invalid."""
    current_age = age_inputs.get("current_age", 0)
    retirement_age = age_inputs.get("retirement_age", 0)
    life_expectancy = age_inputs.get("life_expectancy", 0)
    
    if current_age <= 0:
        return "Current age must be positive"
    if retirement_age <= current_age:
        return "Retirement age must be greater than current age"
    if life_expectancy <= retirement_age:
        return "Life expectancy must be greater than retirement age"
    if current_age > 100:
        return "Current age seems unrealistic (>100)"
    if life_expectancy > 120:
        return "Life expectancy seems unrealistic (>120)"
    
    # Partner validation if exists
    if age_inputs.get("has_partner", False):
        partner_current_age = age_inputs.get("partner_current_age", 0)
        partner_retirement_age = age_inputs.get("partner_retirement_age", 0)
        partner_life_expectancy = age_inputs.get("partner_life_expectancy", 0)
        
        if partner_current_age <= 0:
            return "Partner's current age must be positive"
        if partner_retirement_age <= partner_current_age:
            return "Partner's retirement age must be greater than current age"
        if partner_life_expectancy <= partner_retirement_age:
            return "Partner's life expectancy must be greater than retirement age"
        if partner_current_age > 100:
            return "Partner's current age seems unrealistic (>100)"
        if partner_life_expectancy > 120:
            return "Partner's life expectancy seems unrealistic (>120)"
    
    return None


def validate_financial_inputs(user_inputs: Dict[str, Any]) -> Optional[str]:
    """Validate financial inputs and return error message if invalid."""
    user_income = user_inputs.get("user_annual_income", 0)
    user_expenses = user_inputs.get("user_annual_expenses", 0)
    partner_income = user_inputs.get("partner_annual_income", 0)
    partner_expenses = user_inputs.get("partner_annual_expenses", 0)
    inflation_rate = user_inputs.get("inflation_rate", 0)
    
    if user_income < 0:
        return "Annual income cannot be negative"
    if user_expenses < 0:
        return "Annual expenses cannot be negative"
    if partner_income < 0:
        return "Partner's annual income cannot be negative"
    if partner_expenses < 0:
        return "Partner's annual expenses cannot be negative"
    if inflation_rate < -0.1 or inflation_rate > 0.2:
        return "Inflation rate should be between -10% and 20%"
    
    total_income = user_income + partner_income
    total_expenses = user_expenses + partner_expenses
    
    if total_expenses > total_income * 2:
        return "Annual expenses seem very high compared to income"
    
    return None


def validate_account_data(accounts: list) -> Optional[str]:
    """Validate account data and return error message if invalid."""
    if not accounts:
        return None
    
    for i, account in enumerate(accounts):
        if not hasattr(account, 'name') or not account.name.strip():
            return f"Account {i+1} must have a name"
        if not hasattr(account, 'value') or account.value < 0:
            return f"Account '{account.name}' value cannot be negative"
        if not hasattr(account, 'growth_rate') or account.growth_rate < -0.5 or account.growth_rate > 1.0:
            return f"Account '{account.name}' growth rate should be between -50% and 100%"
    
    return None


def display_validation_errors() -> bool:
    """Check all validations and display errors. Returns True if all valid."""
    errors = []
    
    # Validate age inputs
    age_error = validate_age_inputs(st.session_state.age_inputs)
    if age_error:
        errors.append(f"Age Error: {age_error}")
    
    # Validate financial inputs
    financial_error = validate_financial_inputs(st.session_state.user_inputs)
    if financial_error:
        errors.append(f"Financial Error: {financial_error}")
    
    # Validate account data
    user_account_error = validate_account_data(st.session_state.get("user_accounts", []))
    if user_account_error:
        errors.append(f"User Account Error: {user_account_error}")
    
    partner_account_error = validate_account_data(st.session_state.get("partner_accounts", []))
    if partner_account_error:
        errors.append(f"Partner Account Error: {partner_account_error}")
    
    # Display errors
    if errors:
        st.error("Please fix the following issues:")
        for error in errors:
            st.error(f"• {error}")
        return False
    
    return True