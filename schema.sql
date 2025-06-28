-- Database schema for the financial planner application
-- Run this in your Supabase SQL editor

-- Enable Row Level Security
ALTER TABLE IF EXISTS user_scenarios DISABLE ROW LEVEL SECURITY;
DROP TABLE IF EXISTS user_scenarios;

-- Create user_scenarios table
CREATE TABLE user_scenarios (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    scenario_name TEXT NOT NULL,
    scenario_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Ensure unique scenario names per user
    UNIQUE(user_id, scenario_name)
);

-- Enable Row Level Security
ALTER TABLE user_scenarios ENABLE ROW LEVEL SECURITY;

-- Create policies for user_scenarios table
-- Users can only access their own scenarios
CREATE POLICY "Users can view their own scenarios" ON user_scenarios
    FOR SELECT USING (user_id = current_setting('app.current_user_id', true));

CREATE POLICY "Users can insert their own scenarios" ON user_scenarios
    FOR INSERT WITH CHECK (user_id = current_setting('app.current_user_id', true));

CREATE POLICY "Users can update their own scenarios" ON user_scenarios
    FOR UPDATE USING (user_id = current_setting('app.current_user_id', true))
    WITH CHECK (user_id = current_setting('app.current_user_id', true));

CREATE POLICY "Users can delete their own scenarios" ON user_scenarios
    FOR DELETE USING (user_id = current_setting('app.current_user_id', true));

-- Create indexes for better performance
CREATE INDEX idx_user_scenarios_user_id ON user_scenarios(user_id);
CREATE INDEX idx_user_scenarios_updated_at ON user_scenarios(updated_at DESC);

-- Create a function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_user_scenarios_updated_at 
    BEFORE UPDATE ON user_scenarios 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- For development/testing: temporarily disable RLS if needed
-- You can uncomment this line for testing, but remember to enable RLS in production
-- ALTER TABLE user_scenarios DISABLE ROW LEVEL SECURITY;