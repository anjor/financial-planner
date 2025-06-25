# Supabase Setup Guide

## 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project" and sign up/login
3. Click "New Project"
4. Choose your organization and fill in:
   - Project name: `financial-planner`
   - Database password: (generate a strong password)
   - Region: Choose closest to your users
5. Click "Create new project"

## 2. Get Your Project Keys

1. In your Supabase dashboard, go to **Settings** → **API**
2. Copy these values:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon public key** (long string starting with `eyJ...`)

## 3. Set Up Database Schema

1. In your Supabase dashboard, go to **SQL Editor**
2. Copy and paste the contents of `schema.sql` into a new query
3. Click "Run" to create the database tables and policies

## 4. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Supabase credentials:
   ```
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_KEY=your-anon-public-key-here
   ```

## 5. Install Dependencies

```bash
uv sync
```

## 6. Run the Application

```bash
uv run streamlit run financial_planner.py
```

## 7. Test the Integration

1. The app should now show a login screen
2. Sign up with any email/password (demo authentication)
3. Enter your financial data on the Input page
4. Save scenarios using the Scenarios page
5. Verify data persists between sessions

## Security Notes

- The current implementation uses simplified authentication for demo purposes
- In production, consider using Supabase Auth for proper user management
- Row Level Security (RLS) is enabled to ensure users only see their own data
- Never commit your `.env` file to version control

## Troubleshooting

**Connection Issues:**
- Verify your SUPABASE_URL and SUPABASE_KEY in `.env`
- Check that your Supabase project is active
- Ensure schema.sql was run successfully

**Permission Issues:**
- Verify RLS policies are created correctly
- Check the SQL Editor for any error messages
- Ensure the `user_scenarios` table exists

**Data Not Saving:**
- Check browser console for errors
- Verify network connectivity to Supabase
- Test with a simple scenario first