from google.adk.agents import Agent

from app.agents.prompts.system_prompt import SYSTEM_PROMPT
from app.agents.product import product_agent
from app.agents.inventory import inventory_agent    
from app.agents.sales import sales_agent
from app.agents.customer import customer_agent
from app.agents.analytics import analytics_agent


# from app.tools.product_tool import (
#     search_product,
#     list_products,
# )

# root_agent = Agent(
#     name="supermarket_agent",
#     model="gemini-3.1-flash-lite",
#     description="AI assistant for supermarket operations.",
#     instruction=SYSTEM_PROMPT,
#     tools=[
#         search_product,
#         list_products,
#     ],
# )


from google.adk.agents import Agent

from app.agents.product.product_agent import product_agent
from app.agents.inventory.inventory_agent import inventory_agent
from app.agents.sales.sales_agent import sales_agent
from app.agents.customer.customer_agent import customer_agent
from app.agents.analytics.analytics_agent import analytics_agent


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
    ],
)