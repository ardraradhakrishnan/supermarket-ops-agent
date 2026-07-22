from google.adk.agents import Agent
from app.agents.prompts.billing_prompt import BILLING_PROMPT

from app.tools.billing_tools import (create_bill, get_bill, list_bills,receive_payment, 
                                     get_bill_by_invoice, search_bill, cancel_bill)



billing_agent = Agent(
    name="billing_agent",
    model="gemini-3.1-flash-lite",
    description="Handles billing operations.",
    instruction=BILLING_PROMPT,
    tools=[
        create_bill,
        get_bill,
        list_bills,
        cancel_bill,
        receive_payment, 
        get_bill_by_invoice, search_bill, 
        
    ],
)