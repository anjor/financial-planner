# Financial planner

Basic financial planning tool. Built using extensive help from Claude Sonnet 3.5.

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management. Make sure you have uv installed:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install dependencies:

```bash
# Install all dependencies
uv sync

# Install with development dependencies
uv sync --extra dev
```

## Database Setup

This application uses Supabase for data persistence. See [SUPABASE_SETUP.md](SUPABASE_SETUP.md) for detailed setup instructions.

Quick setup:
1. Create a Supabase project
2. Run the SQL schema from `schema.sql`
3. Copy `.env.example` to `.env` and add your Supabase credentials

## Running the Application

```bash
# Run the Streamlit app
uv run streamlit run financial_planner.py
```

## Development

```bash
# Format code
uv run black .
uv run isort .

# Lint code
uv run ruff check .

# Type checking
uv run mypy .

# Run tests (when available)
uv run pytest
```


## Prompt

>I would like to create a simple website for financial planning for UK residents.
>
>The user should be able to input their income, their current net worth. They should be able to split out the net worth into separate categories highlighting either the tax status such as ISAs vs general investment accounts; and the risk-profile - cash vs invested in broad market index vs crypto.
>
>The user should also be able to input some assumptions such as - retirement age, expected growth of net worth, expected growth of income.
>
>The user should also be able to input their current annual expenses.
>
>Based on this information the app should display interactive plots showing how the wealth will change for the coming years. 
>
>
>First reflect on the project and plan out how you would build it. Highlight different components and choice of technology. 