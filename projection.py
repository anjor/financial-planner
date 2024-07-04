def calculate_projection(
    initial_net_worth,
    annual_income,
    annual_expenses,
    inflation_rate,
    growth_rate,
    years,
    retirement_age,
    current_age,
):
    net_worth = [initial_net_worth]
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

            # Use real growth rate (nominal growth rate - inflation rate)
        real_growth_rate = (1 + growth_rate) / (1 + inflation_rate) - 1
        new_worth = net_worth[-1] * (1 + real_growth_rate) + annual_savings
        net_worth.append(max(0, new_worth))  # Ensure net worth doesn't go negative
    return net_worth
