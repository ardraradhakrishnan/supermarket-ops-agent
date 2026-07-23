# Supermarket Operations Agent

🤖 **Live Telegram Bot:** [@supermarket_ops_demo_bot](https://t.me/supermarket_ops_demo_bot)

A conversational AI assistant that lets a supermarket owner manage their store entirely through natural language — via a Telegram bot. It handles billing, inventory, customer credit (Khata), analytics, and document generation.

---

## 1. Agent Harness

**Framework: Google Agent Development Kit (ADK) with Gemini 1.5 Flash Lite**

ADK was chosen because it provides a first-class multi-agent orchestration model out of the box — a `root_agent` can delegate to typed `sub_agents` without any hand-rolled routing logic. Each domain (billing, inventory, analytics, etc.) lives in its own isolated agent with its own instruction prompt and exact tool list. This keeps prompts short and precise rather than bloating a single mega-prompt, and lets the root agent act as a pure intent router. ADK's `Runner` + `InMemorySessionService` also give per-session conversation memory for free, which is essential for multi-turn sales over Telegram.

---

## 2. Control Loop

The loop runs inside `AgentManager.chat()` in `app/agents/agent_manager.py`:

1. **Observe** — A user message arrives from Telegram and is wrapped in a `Content(role="user")` object.
2. **Reason** — The `Runner` passes the message and session history to the root agent (`supermarket_agent`). The root agent reads its system prompt and decides which sub-agent to delegate to (e.g. `sales_agent`, `analytics_agent`).
3. **Act** — The chosen sub-agent selects a Python tool function (e.g. `create_bill`, `generate_invoice_pdf`) and calls it. The tool opens its own DB session, executes the operation, and returns a structured dict.
4. **Feed result back** — ADK feeds the tool's return value back into the model as a function response. The agent produces a final text reply.
5. **Continue** — The reply is returned to `AgentManager.chat()`, extracted from the async event stream, and sent back to Telegram. Session state is preserved in `InMemorySessionService` keyed by `chat_id`, so the next message picks up where the conversation left off.

---

## 3. Tool Design

Tools are thin Python functions in `app/tools/` that open a DB session, delegate to the relevant service class, and return a plain dict. Each agent receives only the tools it needs.

### Billing & Sales (`billing_tools.py`)

| Tool | Description |
|---|---|
| `create_bill` | Creates a new invoice, reducing inventory and updating Khata atomically |
| `get_bill` | Fetches a bill by numeric ID or invoice number string |
| `list_bills` | Returns all bills ordered newest-first |
| `search_bill` | Full-text search across invoice number, customer name, and phone |
| `cancel_bill` | Cancels a bill and restores inventory stock |
| `receive_payment` | Marks a bill as paid and records the payment method |
| `generate_invoice_pdf` | Renders an HTML invoice and compiles it to PDF via xhtml2pdf |

### Inventory (`inventory_tool.py`)

| Tool | Description |
|---|---|
| `record_purchase` | Adds stock for a product (PURCHASE transaction) |
| `get_stock` | Returns current computed stock for a product |
| `get_stock_history` | Lists all inventory movements for a product |
| `get_low_stock_products` | Returns products at or below the configurable threshold |
| `adjust_stock` | Sets stock to an absolute target via an ADJUSTMENT transaction |

### Products (`product_tool.py`)

| Tool | Description |
|---|---|
| `add_product` | Creates a new product with SKU, price, GST rate, and unit |
| `search_product` | Fuzzy-searches products by name to resolve `product_id` before billing |
| `list_products` | Lists all active products |
| `deactivate_product` | Soft-deletes a product (sets `is_active = False`) |

### Customer (`customer_tool.py`)

| Tool | Description |
|---|---|
| `create_customer` | Registers a new customer with name and phone |
| `get_customer` | Fetches a customer by ID or phone number |
| `search_customer` | Searches customers by name or phone |
| `list_customers` | Lists all registered customers |

### Khata / Credit Ledger (`khata_tool.py`)

| Tool | Description |
|---|---|
| `add_credit` | Records a credit (goods given, payment pending) |
| `add_payment` | Records a payment against outstanding balance |
| `get_balance` | Returns current outstanding balance for a customer |
| `get_ledger` | Returns the full transaction history for a customer |
| `list_pending_customers` | Lists all customers with a positive outstanding balance |

### Analytics (`analytics_tool.py`)

| Tool | Description |
|---|---|
| `get_dashboard_summary` | Returns total products, customers, low-stock count, and pending Khata |
| `get_sales_summary` | Returns today's sales count and revenue |
| `get_top_selling_products` | Returns best-selling products by units sold |
| `get_low_stock_report` | Returns products below threshold with current stock levels |
| `get_recent_sales` | Returns the N most recent bills |
| `get_inventory_value` | Returns the estimated total value of current inventory |
| `generate_sales_report_ppt` | Builds and saves a 4-slide PowerPoint business report |

### Preferences (`preference_tool.py`)

| Tool | Description |
|---|---|
| `get_preference` | Reads a named preference (store name, currency, threshold) |
| `set_preference` | Writes or updates a named preference |

---

## 4. Hard Parts — How Each Was Solved

**Grounding:** The agent is forbidden from inventing product prices, stock levels, or customer data (system prompt rule 2). Every billing and inventory query calls a tool against the live SQLite database. The `sales_agent` is explicitly instructed to always call `search_product` first to resolve a real `product_id` before calling `create_bill` — it cannot skip this step or guess an ID (`SALES_PROMPT` in `app/agents/prompts/sales_prompt.py`).

**Oversell Guard:** `InventoryService.has_stock()` (`app/services/inventory_service.py`) computes current stock by summing all PURCHASE/RETURN transactions and subtracting all SALE/DAMAGE transactions. This check runs **twice** for every sale: once in `BillingService._calculate_bill_totals()` before the bill is written, and again inside `InventoryService.record_sale()` when inventory is actually decremented. If stock falls to zero between those two points the second check raises `InsufficientStockError`, which causes a SQLAlchemy rollback — the bill is never committed.

**GST Correctness:** GST rates are constrained at the database level via a `CheckConstraint` on the `products` table: `gst_rate IN (0, 5, 12, 18, 28)` (`app/models/products.py`). Line-level GST is computed as `unit_price x quantity x gst_rate / 100` using Python `Decimal` arithmetic throughout (`BillingService._calculate_bill_totals` in `app/services/billing_service.py`), avoiding floating-point rounding errors entirely.

**Multi-turn Bills:** ADK's `InMemorySessionService` stores the full conversation history per `session_id` (mapped 1:1 to the Telegram `chat_id` in `AgentManager`). The agent retains bill IDs, product choices, and payment method across multiple messages in the same chat session without any manual state management. A new DB session is opened per tool call, keeping persistence and conversation memory cleanly separated.

**Idempotency:** Invoice numbers are generated with a date-scoped counter: `INV-YYYYMMDD-NNNN` (`BillingService.generate_invoice_number()`). The `invoice_number` column carries a `UNIQUE` constraint, so a duplicate submission will fail at the DB level before any stock or money changes are recorded. Bill cancellation is also idempotent: `cancel_bill` returns immediately if `payment_status` is already `CANCELLED`.

**Concurrency:** SQLite's write-lock serialises concurrent writes. Within a single bill creation, all writes (bill header, bill items, inventory decrements, Khata credit) happen inside a single SQLAlchemy transaction with an explicit `commit()` at the end and a `rollback()` in the except block (`BillingService.create_bill()`). Either the entire operation succeeds together or nothing is written.

**Guardrails:** Each sub-agent's prompt lists **only the tools it is allowed to call** and explicitly forbids calling other agents' tools directly. The system prompt prohibits exposing database tables, SQL, or internal API details to the user. The `is_active` flag on products prevents soft-deleted products from being sold — `_validate_product()` raises `InactiveProductError` if the flag is false.

**Real Artifacts:** PDF invoices are generated in-process by `PDFService.generate_invoice_pdf()` (`app/services/pdf_service.py`) using **xhtml2pdf** (pure Python, no GTK/Cairo dependencies) and saved to `data/invoices/<invoice_number>.pdf`. PowerPoint reports are built slide-by-slide by `PPTService.generate_sales_report_ppt()` (`app/services/ppt_service.py`) using **python-pptx** with embedded matplotlib charts, saved to `data/reports/Report_<timestamp>.pptx`. The Telegram bot handler (`app/bot/telegram_bot.py`) scans the agent text response for file paths using compiled regex patterns (handling both backslash and forward-slash separators), then uploads the file as a Telegram Document attachment.

**Cross-session Memory:** Conversation memory is per-Telegram-chat. `AgentManager` maintains a set of initialised session IDs; on the first message from a chat, `session_service.create_session()` is called once. ADK's `InMemorySessionService` keeps the full message and tool-call history for each session in RAM for the lifetime of the bot process. Persistent cross-restart memory is not implemented — the bot is designed for single-operator use where a restart is rare and acceptable.

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env: set GOOGLE_API_KEY and TELEGRAM_BOT_TOKEN

# 3. Start (initialises DB, seeds data, launches Telegram bot)
python run_bot.py
```

**Live Bot Handle:** `@supermarket_ops_demo_bot`  
**Stack:** Python 3.11+, Google ADK, Gemini 1.5 Flash Lite, SQLAlchemy + SQLite, python-pptx, xhtml2pdf, python-telegram-bot.
