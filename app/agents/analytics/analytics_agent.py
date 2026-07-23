from google.adk.agents import Agent

from app.agents.prompts.analytics_prompt import ANALYTICS_PROMPT
from app.tools.analytics_tool import (get_dashboard_summary, get_sales_summary,get_top_selling_products,
                                      get_customer_outstanding_report, get_low_stock_report, get_inventory_value,
                                      get_recent_sales, generate_sales_report_ppt
                                      )



analytics_agent = Agent(
    name="analytics_agent",
        model="gemini-3.1-flash-lite",
        description="Handles analytics and reporting queries.",
        instruction=ANALYTICS_PROMPT,
    tools=[
        get_dashboard_summary,
        get_sales_summary,
        get_top_selling_products,
        get_customer_outstanding_report,
        get_low_stock_report,
        get_inventory_value,
        get_recent_sales,
        generate_sales_report_ppt,
    ]
)