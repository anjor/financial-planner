from typing import Any


def calculate_projection(
    net_worth_breakdown: dict[str, dict[str, Any]],
    annual_income: float,
    annual_expenses: float,
    inflation_rate: float,
    years_to_project: int,
    retirement_age: int,
    current_age: int
) -> tuple[list[float], dict[str, list[float]]]:
    projection = []
    category_projections = {category: [] for category in net_worth_breakdown.keys()}

    for year in range(years_to_project):
        current_net_worth = sum(category["value"] for category in net_worth_breakdown.values())
        projection.append(current_net_worth)

        for category, data in net_worth_breakdown.items():
            category_projections[category].append(data["value"])

        # Apply growth to all assets
        for category, data in net_worth_breakdown.items():
            data["value"] *= (1 + data["growth"])

        # Apply income and expenses
        if current_age + year < retirement_age:
            # Working years: add income, subtract expenses
            net_change = annual_income - annual_expenses
            # Distribute net change across liquid assets
            liquid_assets = {k: v for k, v in net_worth_breakdown.items() if v.get("is_liquid", True)}
            total_liquid = sum(v["value"] for v in liquid_assets.values())
            if total_liquid > 0 and net_change != 0:
                for data in liquid_assets.values():
                    data["value"] += (data["value"] / total_liquid) * net_change
        else:
            # Retirement: subtract expenses from liquid assets only
            liquid_assets = {k: v for k, v in net_worth_breakdown.items() if v.get("is_liquid", True)}
            total_liquid = sum(v["value"] for v in liquid_assets.values())

            if total_liquid > 0:
                if total_liquid >= annual_expenses:
                    # Reduce liquid assets proportionally
                    for data in liquid_assets.values():
                        data["value"] -= (data["value"] / total_liquid) * annual_expenses
                else:
                    # Not enough liquid assets, withdraw what we can
                    for data in liquid_assets.values():
                        data["value"] = 0

        # Apply inflation to expenses
        annual_expenses *= (1 + inflation_rate)

        current_age += 1

    return projection, category_projections
