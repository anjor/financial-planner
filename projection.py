def calculate_projection(
    net_worth_breakdown,
    annual_income,
    annual_expenses,
    inflation_rate,
    years,
    retirement_age,
    current_age,
):
    net_worth = {
        category: [data["value"]] for category, data in net_worth_breakdown.items()
    }
    total_net_worth = [sum(net_worth[category][0] for category in net_worth)]

    for year in range(1, years + 1):
        # Adjust income and expenses for inflation
        inflated_income = annual_income * (1 + inflation_rate) ** year
        inflated_expenses = annual_expenses * (1 + inflation_rate) ** year

        if current_age + year <= retirement_age:
            annual_savings = inflated_income - inflated_expenses
        else:
            annual_savings = (
                -inflated_expenses
            )  # In retirement, we're drawing down savings

        # Calculate new worth for each category
        for category, data in net_worth_breakdown.items():
            growth_rate = data["growth"]
            real_growth_rate = (1 + growth_rate) / (1 + inflation_rate) - 1

            # Distribute savings/withdrawals proportionally across categories
            category_proportion = (
                net_worth[category][-1] / total_net_worth[-1]
                if total_net_worth[-1] > 0
                else 0
            )
            category_savings = annual_savings * category_proportion

            new_category_worth = (
                net_worth[category][-1] * (1 + real_growth_rate) + category_savings
            )
            net_worth[category].append(max(0, new_category_worth))

        # Calculate total net worth
        new_total_worth = sum(net_worth[category][-1] for category in net_worth)
        total_net_worth.append(max(0, new_total_worth))

    return total_net_worth, net_worth
