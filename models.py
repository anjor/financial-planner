from dataclasses import dataclass
from typing import Dict, List, Optional
from account import HoldingsType


@dataclass
class PersonalInfo:
    """Personal information for an individual."""
    current_age: int
    retirement_age: int
    life_expectancy: int
    annual_income: float
    annual_expenses: float


@dataclass
class FinancialInputs:
    """Combined financial inputs for planning."""
    user: PersonalInfo
    partner: Optional[PersonalInfo]
    inflation_rate: float
    has_partner: bool = False
    
    @property
    def total_annual_income(self) -> float:
        """Calculate total annual income."""
        total = self.user.annual_income
        if self.partner:
            total += self.partner.annual_income
        return total
    
    @property
    def total_annual_expenses(self) -> float:
        """Calculate total annual expenses."""
        total = self.user.annual_expenses
        if self.partner:
            total += self.partner.annual_expenses
        return total


@dataclass
class ProjectionResults:
    """Results from financial projection calculations."""
    total_projection: List[float]
    category_projections: Dict[str, List[float]]
    years: List[int]
    retirement_net_worth: float
    final_net_worth: float
    
    def get_annual_retirement_income(self, withdrawal_rate: float = 0.04) -> float:
        """Calculate estimated annual retirement income using withdrawal rate."""
        return self.retirement_net_worth * withdrawal_rate
    
    def get_years_of_expenses_covered(self, annual_expenses: float) -> float:
        """Calculate how many years of expenses the final net worth covers."""
        if annual_expenses <= 0:
            return 0
        return self.final_net_worth / annual_expenses


def create_financial_inputs_from_session() -> FinancialInputs:
    """Create FinancialInputs object from Streamlit session state."""
    import streamlit as st
    
    user_inputs = st.session_state.user_inputs
    age_inputs = st.session_state.age_inputs
    
    user_info = PersonalInfo(
        current_age=age_inputs["current_age"],
        retirement_age=age_inputs["retirement_age"],
        life_expectancy=age_inputs["life_expectancy"],
        annual_income=user_inputs["user_annual_income"],
        annual_expenses=user_inputs["user_annual_expenses"]
    )
    
    partner_info = None
    if user_inputs.get("has_partner", False):
        partner_info = PersonalInfo(
            current_age=age_inputs["partner_current_age"],
            retirement_age=age_inputs["partner_retirement_age"],
            life_expectancy=age_inputs["partner_life_expectancy"],
            annual_income=user_inputs["partner_annual_income"],
            annual_expenses=user_inputs["partner_annual_expenses"]
        )
    
    return FinancialInputs(
        user=user_info,
        partner=partner_info,
        inflation_rate=user_inputs["inflation_rate"],
        has_partner=user_inputs.get("has_partner", False)
    )