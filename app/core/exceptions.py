"""
Custom exceptions used throughout the application.
"""


class SupermarketException(Exception):
    """
    Base exception for all application-specific errors.
    """

    default_message = "An application error occurred."

    def __init__(self, message: str | None = None):
        super().__init__(message or self.default_message)


# --------------------------------------------------------------------------
# Product Exceptions
# --------------------------------------------------------------------------


class ProductNotFoundError(SupermarketException):
    default_message = "Product not found."


class DuplicateProductError(SupermarketException):
    default_message = "Product already exists."


class InactiveProductError(SupermarketException):
    default_message = "Product is inactive."


# --------------------------------------------------------------------------
# Customer Exceptions
# --------------------------------------------------------------------------


class CustomerNotFoundError(SupermarketException):
    default_message = "Customer not found."


class DuplicateCustomerError(SupermarketException):
    default_message = "Customer already exists."


# --------------------------------------------------------------------------
# Inventory Exceptions
# --------------------------------------------------------------------------


class InventoryError(SupermarketException):
    default_message = "Inventory operation failed."


class InsufficientStockError(InventoryError):
    default_message = "Insufficient stock available."


class InvalidInventoryTransactionError(InventoryError):
    default_message = "Invalid inventory transaction."


# --------------------------------------------------------------------------
# Billing Exceptions
# --------------------------------------------------------------------------


class BillNotFoundError(SupermarketException):
    default_message = "Bill not found."


class InvalidBillError(SupermarketException):
    default_message = "Invalid bill."


class PaymentFailedError(SupermarketException):
    default_message = "Payment failed."


# --------------------------------------------------------------------------
# Khata Exceptions
# --------------------------------------------------------------------------


class KhataError(SupermarketException):
    default_message = "Khata operation failed."


class InsufficientPaymentError(KhataError):
    default_message = "Payment amount is insufficient."


# --------------------------------------------------------------------------
# Preference Exceptions
# --------------------------------------------------------------------------


class PreferenceNotFoundError(SupermarketException):
    default_message = "Preference not found."


# --------------------------------------------------------------------------
# AI / Request Exceptions
# --------------------------------------------------------------------------


class ProcessRequestError(SupermarketException):
    default_message = "Unable to process the request."


class DuplicateRequestError(ProcessRequestError):
    default_message = "Request has already been processed."


# --------------------------------------------------------------------------
# Validation Exceptions
# --------------------------------------------------------------------------


class ValidationError(SupermarketException):
    default_message = "Validation failed."


class BusinessRuleViolation(SupermarketException):
    default_message = "Business rule violated."