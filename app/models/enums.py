from enum import Enum


class Unit(str, Enum):
    PIECE = "piece"
    KG = "kg"
    GRAM = "gram"
    LITRE = "litre"
    ML = "ml"
    PACK = "pack"
    BOX = "box"


class InventoryTransactionType(str, Enum):
    PURCHASE = "PURCHASE"
    SALE = "SALE"
    RETURN = "RETURN"
    DAMAGE = "DAMAGE"
    ADJUSTMENT = "ADJUSTMENT"


class PaymentMethod(str, Enum):
    CASH = "CASH"
    UPI = "UPI"
    CARD = "CARD"
    CREDIT = "CREDIT"


class PaymentStatus(str, Enum):
    PAID = "PAID"
    PENDING = "PENDING"
    PARTIALLY_PAID = "PARTIALLY_PAID"


class KhataTransactionType(str, Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"