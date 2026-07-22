from google.adk.agents import Agent

from app.agents.prompts.product_prompt import PRODUCT_PROMPT
from app.tools.product_tool import (search_product, list_products,create_product,update_product,
                                    deactivate_product)



product_agent = Agent(
    name="product_agent",
    model="gemini-3.1-flash-lite",
    description="Handles product catalog queries.",
    instruction=PRODUCT_PROMPT,
    tools=[
        search_product,
        list_products,
        create_product,
        update_product,
        deactivate_product,
    ],
)