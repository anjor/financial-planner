# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

UK Financial Planning Tool - A Streamlit-based web application for financial planning and retirement projections for UK residents. Built with Python 3.13, using Streamlit for UI, Plotly for visualizations, and Supabase for data persistence.

## Development Commands

```bash
# Install dependencies
uv sync
uv sync --extra dev  # Include dev dependencies

# Run the application
uv run streamlit run financial_planner.py

# Code quality
uv run black .          # Format code
uv run isort .          # Sort imports
uv run ruff check .     # Lint code
uv run mypy .           # Type checking
uv run pytest           # Run tests (when available)
```

## Architecture Overview

### Core Application Flow
1. **Entry Point**: `financial_planner.py` - Initializes Streamlit config, manages authentication, and handles page navigation
2. **State Management**: All user data stored in `st.session_state`, initialized by `state.py`
3. **Page Structure**: Three main pages - Input (data entry), Results (projections), Scenarios (save/load)

### Key Architectural Patterns

**Data Flow**: User Input → Session State → Validation → Projection Calculations → Visualization
- Session state is the single source of truth during a session
- Data persistence to Supabase is optional via scenarios
- All calculations happen in-memory per session

**Asset Management**:
- Assets are classified as liquid (Cash, S&S) or illiquid (Property, Other)
- During working years: income/expenses only affect liquid assets
- During retirement: liquid assets drawn down first, illiquid assets sold only when needed
- Growth rates applied to all assets regardless of liquidity

**Authentication**: Currently a mock system (any email/password works)
- User IDs generated from email hash
- No actual user table or password verification
- Session-based only, lost on refresh

### Critical Implementation Details

1. **Projection Engine** (`projection.py`):
   - Iterates year by year from current age to life expectancy
   - Applies growth rates before income/expenses
   - Working years: net savings/deficit distributed proportionally across liquid assets
   - Retirement: expenses withdrawn from liquid assets first, then illiquid if needed

2. **Database Schema**:
   - Single table: `user_scenarios` with JSONB storage
   - Row Level Security ensures users only see their own data
   - No user authentication table (relies on mock auth)

3. **State Structure**:
   - `user_inputs`: Income, expenses, net worth
   - `age_inputs`: Current age, retirement age, life expectancy  
   - `{user|partner}_accounts`: List of Account objects with holdings type
   - `{user|partner}_net_worth_breakdown`: Dict with value, growth, is_liquid

## Environment Setup

Required environment variables in `.env`:
```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key-here
```

## Common Development Tasks

### Adding New Asset Types
1. Add to `HoldingsType` enum in `account.py` with liquidity flag
2. Update UI in `inputs/assets.py` if needed
3. Test drawdown behavior in retirement scenarios

### Modifying Financial Calculations
- Core logic in `projection.py` - `calculate_projection()` function
- Results processing in `results.py` - `_combine_net_worth_breakdowns()`
- Ensure liquid vs illiquid asset handling is preserved

### Working with Scenarios
- Scenarios serialize entire session state to JSONB
- Loading scenarios overwrites all session state
- Database operations in `database.py` - `DatabaseManager` class


## Development notes

- ALWAYS create branches to do your work. Before creating a branch make sure you have
  pulled the latest main.
- Keep CLAUDE.md up to date. If there is out of date information update it.
