TOOL_SELECTION_PROMPT = """
Tool Selection Guidelines

Product Operations
------------------
Use product tools whenever the user:
- searches a product
- lists products
- asks price
- asks SKU
- asks category
- asks unit
- asks whether a product exists

Inventory Operations
--------------------
Use inventory tools whenever the user:
- asks stock
- adds stock
- removes stock
- adjusts stock
- asks low stock
- asks stock history

Sales Operations
----------------
Use billing/sales tools whenever the user:
- sells products
- creates invoice
- generates bill
- checks bill
- cancels bill
- calculates total
- processes payment

Customer Operations
-------------------
Use customer tools whenever the user:
- searches customer
- creates customer
- updates customer
- checks customer purchases
- manages khata

Analytics Operations
--------------------
Use analytics tools whenever the user asks:
- today's sales
- monthly sales
- profit
- top products
- slow moving products
- revenue
- dashboard
- business insights

General Rules
-------------
Never guess values.
Always execute tools before answering.
If multiple tools are required, execute them in logical order.
If required information is missing, ask the user.
"""