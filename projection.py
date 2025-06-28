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
            # Distribute net change across liquid assets only
            liquid_assets = {k: v for k, v in net_worth_breakdown.items() if v.get("is_liquid", True)}
            total_liquid = sum(v["value"] for v in liquid_assets.values())
            
            if net_change > 0:
                # Savings: distribute across liquid assets
                if total_liquid > 0:
                    for data in liquid_assets.values():
                        data["value"] += (data["value"] / total_liquid) * net_change
                else:
                    # No liquid assets, create a default cash account
                    if liquid_assets:
                        # Add to first liquid asset category
                        list(liquid_assets.values())[0]["value"] += net_change
            elif net_change < 0 and total_liquid > 0:
                # Deficit: reduce liquid assets proportionally
                for data in liquid_assets.values():
                    data["value"] += (data["value"] / total_liquid) * net_change
                    # Ensure we don't go negative
                    if data["value"] < 0:
                        data["value"] = 0
        else:
            # Retirement: subtract expenses from assets
            liquid_assets = {k: v for k, v in net_worth_breakdown.items() if v.get("is_liquid", True)}
            illiquid_assets = {k: v for k, v in net_worth_breakdown.items() if not v.get("is_liquid", True)}
            total_liquid = sum(v["value"] for v in liquid_assets.values())

            if total_liquid >= annual_expenses:
                # Enough liquid assets: reduce them proportionally
                for data in liquid_assets.values():
                    data["value"] -= (data["value"] / total_liquid) * annual_expenses
            else:
                # Not enough liquid assets
                remaining_expenses = annual_expenses - total_liquid
                
                # First, use up all liquid assets
                for data in liquid_assets.values():
                    data["value"] = 0
                
                # Then, sell illiquid assets if needed
                if remaining_expenses > 0 and illiquid_assets:
                    # Sort illiquid assets by value (sell smallest first)
                    sorted_illiquid = sorted(illiquid_assets.items(), key=lambda x: x[1]["value"])
                    
                    for category, data in sorted_illiquid:
                        if remaining_expenses <= 0:
                            break
                        
                        if data["value"] >= remaining_expenses:
                            # Convert part of this illiquid asset to liquid
                            # In reality, this might represent downsizing or partial sale
                            data["value"] -= remaining_expenses
                            remaining_expenses = 0
                        else:
                            # Sell entire illiquid asset
                            remaining_expenses -= data["value"]
                            data["value"] = 0

        # Apply inflation to expenses
        annual_expenses *= (1 + inflation_rate)

        current_age += 1

    return projection, category_projections
