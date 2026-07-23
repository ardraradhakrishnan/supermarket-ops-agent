from google.adk.agents import Agent
from app.agents.prompts.sales_prompt import SALES_PROMPT
from app.tools.billing_tools import (
    create_bill,
    get_bill,
    list_bills,
    cancel_bill,
    receive_payment,
    get_bill_by_invoice,
    search_bill,
    generate_invoice_pdf,
)

from app.tools.product_tool import (
    search_product,
    list_products,
)

sales_agent = Agent(
    name="sales_agent",
    model="gemini-3.1-flash-lite",
    description="Handles sales and billing operations.",
    instruction=SALES_PROMPT,
    tools=[
        create_bill,
        get_bill,
        list_bills,
        cancel_bill,
        receive_payment,
        get_bill_by_invoice,
        search_bill,
        generate_invoice_pdf,
        search_product,
        list_products,
    ],
)
