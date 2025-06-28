"""Database interface for Supabase integration."""

import json
import os
from typing import Any

import streamlit as st
from dotenv import load_dotenv
from supabase import Client, create_client

# Load environment variables
load_dotenv()


class SupabaseClient:
    """Supabase client wrapper for the financial planner app."""

    def __init__(self):
        self._client: Client | None = None
        self._initialize_client()

    def _initialize_client(self) -> None:
        """Initialize Supabase client with environment variables."""
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

        if not url or not key:
            st.error("⚠️ Supabase configuration missing. Please set SUPABASE_URL and SUPABASE_KEY in your .env file.")
            return

        try:
            self._client = create_client(url, key)
        except Exception as e:
            st.error(f"Failed to initialize Supabase client: {str(e)}")

    @property
    def client(self) -> Client | None:
        """Get the Supabase client."""
        return self._client

    def is_connected(self) -> bool:
        """Check if the client is properly connected."""
        return self._client is not None


class DatabaseManager:
    """Database operations manager for the financial planner."""

    def __init__(self):
        self.supabase = SupabaseClient()

    def save_user_scenario(self, user_id: str, scenario_name: str, scenario_data: dict[str, Any]) -> bool:
        """Save a financial scenario for a user."""
        if not self.supabase.is_connected():
            return False

        try:
            # Prepare data for insertion
            data = {
                "user_id": user_id,
                "scenario_name": scenario_name,
                "scenario_data": json.dumps(scenario_data),
                "updated_at": "now()"
            }

            # Check if scenario already exists
            existing = self.supabase.client.table("user_scenarios").select("id").eq("user_id", user_id).eq("scenario_name", scenario_name).execute()

            if existing.data:
                # Update existing scenario
                result = self.supabase.client.table("user_scenarios").update(data).eq("user_id", user_id).eq("scenario_name", scenario_name).execute()
            else:
                # Insert new scenario
                result = self.supabase.client.table("user_scenarios").insert(data).execute()

            return len(result.data) > 0

        except Exception as e:
            st.error(f"Failed to save scenario: {str(e)}")
            return False

    def load_user_scenario(self, user_id: str, scenario_name: str) -> dict[str, Any] | None:
        """Load a specific scenario for a user."""
        if not self.supabase.is_connected():
            return None

        try:
            result = self.supabase.client.table("user_scenarios").select("scenario_data").eq("user_id", user_id).eq("scenario_name", scenario_name).execute()

            if result.data:
                return json.loads(result.data[0]["scenario_data"])
            return None

        except Exception as e:
            st.error(f"Failed to load scenario: {str(e)}")
            return None

    def list_user_scenarios(self, user_id: str) -> list[dict[str, Any]]:
        """List all scenarios for a user."""
        if not self.supabase.is_connected():
            return []

        try:
            result = self.supabase.client.table("user_scenarios").select("scenario_name, created_at, updated_at").eq("user_id", user_id).order("updated_at", desc=True).execute()
            return result.data or []

        except Exception as e:
            st.error(f"Failed to list scenarios: {str(e)}")
            return []

    def delete_user_scenario(self, user_id: str, scenario_name: str) -> bool:
        """Delete a specific scenario for a user."""
        if not self.supabase.is_connected():
            return False

        try:
            result = self.supabase.client.table("user_scenarios").delete().eq("user_id", user_id).eq("scenario_name", scenario_name).execute()
            return len(result.data) > 0

        except Exception as e:
            st.error(f"Failed to delete scenario: {str(e)}")
            return False


# Global instance
db_manager = DatabaseManager()


def get_db_manager() -> DatabaseManager:
    """Get the global database manager instance."""
    return db_manager
