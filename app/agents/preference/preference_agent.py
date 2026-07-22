from google.adk.agents import Agent
from app.agents.prompts.preference_prompt import PREFERENCE_PROMPT
from app.tools.preference_tool import (get_store_name, get_currency, get_low_stock_threshold,
                                        get_preference, update_preference  )



preference_agent = Agent(
    name="preference_agent",
    model="gemini-3.1-flash-lite",
    description="Handles preference operations.",
    instruction=PREFERENCE_PROMPT,
    tools=[
        get_store_name,
        get_currency,
        get_low_stock_threshold,
        get_preference,
        update_preference
    ],
)