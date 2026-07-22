from app.models.products import Product
from app.models.khata import KhataTransaction



def serialize_product(
    product: Product,
) -> dict:
    """
    Convert Product ORM object to dictionary.
    """

    return {
        "id": product.id,
        "sku": product.sku,
        "name": product.name,
        "description": product.description,
        "price": float(product.unit_price),
        "gst_rate": product.gst_rate,
        "unit": product.unit.value,
        "active": product.is_active,
    }


def serialize_products(
    products: list[Product],
) -> list[dict]:
    """
    Convert list of Product ORM objects.
    """

    return [
        serialize_product(product)
        for product in products
    ]

def serialize_inventory_transaction(transaction):

    return {
        "id": transaction.id,
        "product_id": transaction.product_id,
        "transaction_type": transaction.transaction_type.value,
        "quantity": float(transaction.quantity),
        "reference": transaction.reference,
        "remarks": transaction.remarks,
        "created_at": transaction.created_at.isoformat(),
    }


def serialize_inventory_transactions(transactions):

    return [
        serialize_inventory_transaction(tx)
        for tx in transactions
    ]


def serialize_customer(customer):

    return {
        "id": customer.id,
        "name": customer.name,
        "phone": customer.phone,
        "email": customer.email,
        "address": customer.address,
        "is_active": customer.is_active,
    }


def serialize_customers(customers):

    return [
        serialize_customer(customer)
        for customer in customers
    ]


def serialize_bills(bills) -> list[dict]:
    """
    Serialize a list of bills.
    """

    return [
        serialize_bill(bill)
        for bill in bills
    ]

def serialize_bill(bill) -> dict:
    """
    Serialize a bill with items.
    """

    return {
        "id": bill.id,
        "invoice_number": bill.invoice_number,
        "customer_id": bill.customer_id,
        "customer_name": (
            bill.customer.name
            if bill.customer
            else None
        ),
        "subtotal": float(bill.subtotal),
        "discount": float(bill.discount),
        "tax": float(bill.tax),
        "total": float(bill.total),
        "paid_amount": float(bill.paid_amount),
        "payment_method": (
            bill.payment_method.value
            if bill.payment_method
            else None
        ),
        "payment_status": (
            bill.payment_status.value
            if bill.payment_status
            else None
        ),
        "status": (
            bill.status.value
            if bill.status
            else None
        ),
        "items": [
            {
                "product": item.product.name,
                "quantity": float(item.quantity),
                "unit_price": float(item.unit_price),
                "total": float(item.total),
            }
            for item in bill.items
        ],
        "created_at": (
            bill.created_at.isoformat()
            if bill.created_at
            else None
        ),
    }




def serialize_khata_transaction(
    transaction: KhataTransaction,
) -> dict:
    """
    Serializes a Khata transaction.
    """

    return {
        "id": transaction.id,
        "customer_id": transaction.customer_id,
        "transaction_type": transaction.transaction_type.value,
        "amount": float(transaction.amount),
        "remarks": transaction.remarks,
        "created_at": (
            transaction.created_at.isoformat()
            if transaction.created_at
            else None
        ),
        "updated_at": (
            transaction.updated_at.isoformat()
            if transaction.updated_at
            else None
        ),
    }


def serialize_khata_transactions(
    transactions: list[KhataTransaction],
) -> list[dict]:
    """
    Serializes a list of Khata transactions.
    """

    return [
        serialize_khata_transaction(tx)
        for tx in transactions
    ]