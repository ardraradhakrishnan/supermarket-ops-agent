from .system_prompt import SYSTEM_PROMPT
from .tool_selection_prompt import TOOL_SELECTION_PROMPT
from .product_prompt import PRODUCT_PROMPT
from .inventory_prompt import INVENTORY_PROMPT
from .sales_prompt import SALES_PROMPT
from .customer_prompt import CUSTOMER_PROMPT
from .analytics_prompt import ANALYTICS_PROMPT


ROOT_PROMPT = "\n\n".join(
    [
        SYSTEM_PROMPT,
        TOOL_SELECTION_PROMPT,
        PRODUCT_PROMPT,
        INVENTORY_PROMPT,
        SALES_PROMPT,
        CUSTOMER_PROMPT,
        ANALYTICS_PROMPT,
    ]
)