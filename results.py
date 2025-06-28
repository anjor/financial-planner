from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from projection import calculate_projection
from validation import display_validation_errors


def _combine_net_worth_breakdowns(inputs: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Combine user and partner net worth breakdowns."""
    combined_net_worth_breakdown = {}
    for category in set(inputs["user_net_worth_breakdown"].keys()) | set(
        inputs["partner_net_worth_breakdown"].keys()
    ):
        combined_value = (
            inputs["user_net_worth_breakdown"].get(category, {"value": 0})["value"]
            + inputs["partner_net_worth_breakdown"].get(category, {"value": 0})["value"]
        )
        combined_growth = max(
            inputs["user_net_worth_breakdown"].get(category, {"growth": 0})["growth"],
            inputs["partner_net_worth_breakdown"].get(category, {"growth": 0})[
                "growth"
            ],
        )
        # Determine liquidity (if either user or partner has liquid version, it's liquid)
        user_liquid = inputs["user_net_worth_breakdown"].get(category, {}).get("is_liquid", False)
        partner_liquid = inputs["partner_net_worth_breakdown"].get(category, {}).get("is_liquid", False)
        is_liquid = user_liquid or partner_liquid

        combined_net_worth_breakdown[category] = {
            "value": combined_value,
            "growth": combined_growth,
            "is_liquid": is_liquid,
        }
    return combined_net_worth_breakdown


def _create_projection_dataframe(
    projection: list[float],
    category_projections: dict[str, list[float]],
    age_inputs: dict[str, Any]
) -> pd.DataFrame:
    """Create DataFrame for plotting from projection data."""
    return pd.DataFrame(
        {
            "Year": range(age_inputs["current_age"], age_inputs["life_expectancy"] + 1),
            "Total Net Worth": projection,
            **{category: values for category, values in category_projections.items()},
        }
    )


def _plot_total_net_worth(df: pd.DataFrame, age_inputs: dict[str, Any]) -> None:
    """Plot total net worth over time."""
    fig_total = px.line(
        df,
        x="Year",
        y="Total Net Worth",
        title="Projected Combined Net Worth Over Lifetime",
    )
    fig_total.update_layout(yaxis_title="Net Worth (£)")
    fig_total.add_vline(
        x=age_inputs["retirement_age"],
        line_dash="dash",
        line_color="red",
        annotation_text="Retirement Age",
        annotation_position="top right",
    )
    st.plotly_chart(fig_total)


def _plot_net_worth_breakdown(df: pd.DataFrame, category_projections: dict[str, list[float]]) -> None:
    """Plot breakdown of net worth over time."""
    fig_breakdown = go.Figure()
    for category in category_projections.keys():
        fig_breakdown.add_trace(
            go.Scatter(x=df["Year"], y=df[category], name=category, stackgroup="one")
        )
    fig_breakdown.update_layout(
        title="Net Worth Breakdown Over Time", yaxis_title="Net Worth (£)"
    )
    st.plotly_chart(fig_breakdown)


def _display_key_metrics(
    projection: list[float],
    age_inputs: dict[str, Any],
    total_annual_expenses: float
) -> None:
    """Display key retirement metrics."""
    retirement_net_worth = projection[
        age_inputs["retirement_age"] - age_inputs["current_age"]
    ]
    final_net_worth = projection[-1]

    st.header("Key Metrics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Net Worth at Retirement", f"£{retirement_net_worth:,.0f}")
        st.metric("Final Net Worth", f"£{final_net_worth:,.0f}")
    with col2:
        annual_retirement_income = retirement_net_worth * 0.04  # Using the 4% rule
        st.metric(
            "Estimated Annual Retirement Income (4% Rule)",
            f"£{annual_retirement_income:,.0f}",
        )
        years_of_expenses = final_net_worth / total_annual_expenses if total_annual_expenses > 0 else 0
        st.metric("Years of Expenses Covered", f"{years_of_expenses:.1f}")


def _display_current_figures(
    total_annual_income: float,
    total_annual_expenses: float,
    combined_net_worth_breakdown: dict[str, dict[str, Any]]
) -> None:
    """Display current combined financial figures."""
    st.header("Current Combined Figures")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Annual Income", f"£{total_annual_income:,.0f}")
        st.metric("Total Annual Expenses", f"£{total_annual_expenses:,.0f}")
    with col2:
        total_net_worth = sum(
            data["value"] for data in combined_net_worth_breakdown.values()
        )
        st.metric("Total Current Net Worth", f"£{total_net_worth:,.0f}")
        savings_rate = (
            (total_annual_income - total_annual_expenses) / total_annual_income * 100
            if total_annual_income > 0 else 0
        )
        st.metric("Savings Rate", f"{savings_rate:.1f}%")


def _display_net_worth_breakdown(combined_net_worth_breakdown: dict[str, dict[str, Any]]) -> None:
    """Display current net worth breakdown table."""
    st.header("Current Net Worth Breakdown")
    breakdown_df = pd.DataFrame(
        [
            {
                "Category": category,
                "Value": data["value"],
                "Growth Rate": f"{data['growth']*100:.1f}%",
                "Liquidity": "Liquid" if data.get("is_liquid", False) else "Non-liquid"
            }
            for category, data in combined_net_worth_breakdown.items()
        ]
    )
    breakdown_df = breakdown_df.sort_values("Value", ascending=False)
    st.table(breakdown_df)


def _display_retirement_assessment(
    projection: list[float],
    age_inputs: dict[str, Any],
    total_annual_expenses: float
) -> None:
    """Display retirement readiness assessment."""
    retirement_net_worth = projection[
        age_inputs["retirement_age"] - age_inputs["current_age"]
    ]

    st.header("Retirement Readiness Assessment")
    if retirement_net_worth >= total_annual_expenses * 25:
        st.success("You're on track for a comfortable retirement!")
    elif retirement_net_worth >= total_annual_expenses * 15:
        st.warning(
            "You're making progress, but might want to consider increasing your savings."
        )
    else:
        st.error(
            "You may need to significantly increase your savings or adjust your retirement plans."
        )


def show_results_page() -> None:
    """Main function to display the results page."""
    st.title("UK Financial Planning Tool - Results")

    # Validate inputs before showing results
    if not display_validation_errors():
        st.warning("Please go to the Input page and fix the validation errors before viewing results.")
        return

    inputs = st.session_state.user_inputs
    age_inputs = st.session_state.age_inputs

    # Combine user and partner data
    combined_net_worth_breakdown = _combine_net_worth_breakdowns(inputs)
    total_annual_income = inputs["user_annual_income"] + inputs["partner_annual_income"]
    total_annual_expenses = (
        inputs["user_annual_expenses"] + inputs["partner_annual_expenses"]
    )
    years_to_project = age_inputs["life_expectancy"] - age_inputs["current_age"]

    # Calculate projection
    projection, category_projections = calculate_projection(
        combined_net_worth_breakdown,
        total_annual_income,
        total_annual_expenses,
        inputs["inflation_rate"],
        years_to_project,
        age_inputs["retirement_age"],
        age_inputs["current_age"],
    )

    # Create DataFrame and display results
    df = _create_projection_dataframe(projection, category_projections, age_inputs)

    # Display all components
    _plot_total_net_worth(df, age_inputs)
    _plot_net_worth_breakdown(df, category_projections)
    _display_key_metrics(projection, age_inputs, total_annual_expenses)
    _display_current_figures(total_annual_income, total_annual_expenses, combined_net_worth_breakdown)
    _display_net_worth_breakdown(combined_net_worth_breakdown)
    _display_retirement_assessment(projection, age_inputs, total_annual_expenses)
