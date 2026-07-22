from google.adk.agents import Agent
from app.agents.prompts.khata_prompt import KHATA_PROMPT
from app.tools.khata_tool import (add_credit, add_payment, get_balance, get_ledger, clear_balance,
                                  search_customer_ledger, list_pending_customers, get_total_outstanding, get_top_debtors,
                                  get_top_debtors, )





khata_agent = Agent(
    name="khata_agent",
    model="gemini-3.1-flash-lite",
    description="Handles khata operations.",
    instruction=KHATA_PROMPT,
    tools=[
        add_credit, 
        add_payment,
        get_balance,
        get_ledger,
        clear_balance,
        search_customer_ledger,
        list_pending_customers,
        get_total_outstanding,
        get_top_debtors,
    ],
)