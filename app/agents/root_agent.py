from google.adk.agents import Agent

from app.agents.prompts.system_prompt import SYSTEM_PROMPT
from app.agents.product.product_agent import product_agent
from app.agents.inventory.inventory_agent import inventory_agent
from app.agents.salesworkflow.sales_agent import sales_agent
from app.agents.customer.customer_agent import customer_agent
from app.agents.analytics.analytics_agent import analytics_agent
from app.agents.khata.khata_agent import khata_agent
from app.agents.preference.preference_agent import preference_agent


root_agent = Agent(
    name="supermarket_agent",
    model="gemini-3.1-flash-lite",
    description="AI assistant for supermarket operations.",
    instruction=SYSTEM_PROMPT,
    sub_agents=[
        product_agent,
        inventory_agent,
        sales_agent,
        customer_agent,
        analytics_agent,
        khata_agent,
        preference_agent,
    ],
)