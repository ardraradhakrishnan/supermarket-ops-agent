from google.adk.agents import Agent
from app.agents.prompts.customer_prompt import CUSTOMER_PROMPT
from app.tools.customer_tool import (search_customer, list_customers, get_customer, get_walkin_customer,
                                     create_customer, update_customer, deactivate_customer,get_customer_by_phone)   



customer_agent = Agent(
    name="customer_agent",
    model="gemini-3.1-flash-lite",
    description="Handles customer management queries.",
    instruction=CUSTOMER_PROMPT,
    tools=[
        search_customer,
        list_customers,
        get_customer,
        get_walkin_customer,
        create_customer,
        update_customer,
        deactivate_customer,  
        get_customer_by_phone
    ],
)