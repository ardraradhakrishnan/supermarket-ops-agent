from google.adk.agents import Agent
from app.agents.prompts.inventory_prompt import INVENTORY_PROMPT
from app.tools.inventory_tool import (get_current_stock, get_stock_history, get_low_stock_products, adjust_stock,
                                      record_purchase, record_sale)





inventory_agent = Agent(
    name="inventory_agent",
    model="gemini-3.1-flash-lite",
    description="Handles inventory operations.",
    instruction=INVENTORY_PROMPT,
    tools=[
        get_current_stock,
        get_stock_history,
        get_low_stock_products,
        adjust_stock,
        record_purchase,
        record_sale,
    ],
)