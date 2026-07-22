from datetime import datetime
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import (
    BillNotFoundError,
    CustomerNotFoundError,
    ProductNotFoundError,
    InactiveProductError,
    InsufficientStockError,
)

from app.models.billing import Bill, BillItem
from app.models.customer import Customer
from app.models.products import Product

from app.models.enums import (
    PaymentMethod,
    PaymentStatus,
    InventoryTransactionType,
    KhataTransactionType,
)

from app.schemas.billing import BillCreate
from app.schemas.inventory import InventoryTransactionCreate
from app.schemas.khata import KhataTransactionCreate

from app.services.base_service import BaseService
from app.services.customer_service import CustomerService
from app.services.inventory_service import InventoryService
from app.services.khata_service import KhataService
from app.services.product_service import ProductService


class BillingService(BaseService):
    """
    Handles invoice creation and billing operations.
    """

    def __init__(
        self,
        db: Session,
    ):
        super().__init__(db)

        self.product_service = ProductService(db)
        self.customer_service = CustomerService(db)
        self.inventory_service = InventoryService(db)
        self.khata_service = KhataService(db)

    def generate_invoice_number(self) -> str:
        """
        Generates the next invoice number.
        """

        today = datetime.now().strftime("%Y%m%d")

        count = self.scalar(
            select(
                func.count(Bill.id)
            ).where(
                Bill.invoice_number.like(
                    f"INV-{today}%"
                )
            )
        )

        return f"INV-{today}-{count + 1:04d}"

    def _validate_customer(
        self,
        customer_id: int | None,
    ) -> Customer | None:
        """
        Validates customer existence.
        """

        if customer_id is None:
            return None

        customer = self.customer_service.get_by_id(
            customer_id
        )

        if customer is None:
            raise CustomerNotFoundError()

        return customer

    def _validate_product(
        self,
        product_id: int,
    ) -> Product:
        """
        Validates product existence.
        """

        product = self.product_service.get_by_id(
            product_id
        )

        if product is None:
            raise ProductNotFoundError()

        if not product.is_active:
            raise InactiveProductError()

        return product
    
    def _calculate_bill_totals(
        self,
        bill_data: BillCreate,
    ) -> tuple[
        Decimal,
        Decimal,
        Decimal,
        list[BillItem],
    ]:
        """
        Calculates bill totals and prepares BillItem ORM objects.
        """

        subtotal = Decimal("0.00")
        gst_amount = Decimal("0.00")

        bill_items: list[BillItem] = []

        for item in bill_data.items:

            product = self._validate_product(
                item.product_id
            )

            if not self.inventory_service.has_stock(
                product.id,
                item.quantity,
            ):
                raise InsufficientStockError(
                    f"Insufficient stock for '{product.name}'."
                )

            line_total = (
                product.unit_price
                * item.quantity
            )

            line_gst = (
                line_total
                * Decimal(product.gst_rate)
                / Decimal("100")
            )

            subtotal += line_total
            gst_amount += line_gst

            bill_item = BillItem(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.unit_price,
                gst_amount=line_gst,
                line_total=line_total,
            )

            bill_items.append(
                bill_item
            )

        discount = (
            bill_data.discount
            if bill_data.discount
            else Decimal("0.00")
        )

        grand_total = (
            subtotal
            + gst_amount
            - discount
        )

        if grand_total < 0:
            grand_total = Decimal("0.00")

        return (
            subtotal,
            gst_amount,
            grand_total,
            bill_items,
        )
    
    def create_bill(
        self,
        bill_data: BillCreate,
    ) -> Bill:
        """
        Creates a new invoice.

        Workflow
        --------
        1. Validate customer
        2. Validate products
        3. Calculate totals
        4. Create bill
        5. Create bill items
        6. Reduce inventory
        7. Create Khata entry (if credit sale)
        8. Commit transaction
        """

        # Credit sales must have a customer
        if (
            bill_data.payment_method
            == PaymentMethod.CREDIT
            and bill_data.customer_id is None
        ):
            raise CustomerNotFoundError(
                "Credit sale requires a customer."
            )

        self._validate_customer(
            bill_data.customer_id
        )

        (
            subtotal,
            gst_amount,
            grand_total,
            bill_items,
        ) = self._calculate_bill_totals(
            bill_data
        )

        payment_status = (
            PaymentStatus.PENDING
            if bill_data.payment_method
            == PaymentMethod.CREDIT
            else PaymentStatus.PAID
        )

        bill = Bill(
            invoice_number=self.generate_invoice_number(),
            customer_id=bill_data.customer_id,
            subtotal=subtotal,
            gst_amount=gst_amount,
            discount=bill_data.discount,
            grand_total=grand_total,
            payment_method=bill_data.payment_method,
            payment_status=payment_status,
        )

        try:

            # -------------------------
            # Create Bill Header
            # -------------------------

            self.add(bill)
            self.flush()
            self.refresh(bill)

            # -------------------------
            # Create Bill Items
            # -------------------------

            for item in bill_items:
                item.bill_id = bill.id

            self.add_all(bill_items)

            # -------------------------
            # Reduce Inventory
            # -------------------------

            for item in bill_data.items:

                inventory_transaction = (
                    InventoryTransactionCreate(
                        product_id=item.product_id,
                        quantity=item.quantity,
                        transaction_type=InventoryTransactionType.STOCK_OUT,
                        remarks=f"Invoice {bill.invoice_number}",
                    )
                )

                self.inventory_service.stock_out(
                    inventory_transaction
                )

            # -------------------------
            # Update Khata
            # -------------------------

            if (
                bill.payment_method
                == PaymentMethod.CREDIT
            ):

                khata_transaction = (
                    KhataTransactionCreate(
                        customer_id=bill.customer_id,
                        amount=grand_total,
                        transaction_type=KhataTransactionType.CREDIT,
                        remarks=f"Invoice {bill.invoice_number}",
                    )
                )

                self.khata_service.add_credit(
                    khata_transaction
                )

            # -------------------------
            # Final Commit
            # -------------------------

            self.commit()

            self.refresh(bill)

            return bill

        except Exception:

            self.rollback()

            raise

    def get_bill(
        self,
        bill_id: int,
    ) -> Bill:
        """
        Returns a bill by its ID.
        """

        bill = self.scalar(
            select(Bill).where(
                Bill.id == bill_id
            )
        )

        if bill is None:
            raise BillNotFoundError()

        return bill
    
    def get_bill_by_invoice(
        self,
        invoice_number: str,
    ) -> Bill:
        """
        Returns a bill using its invoice number.
        """

        bill = self.scalar(
            select(Bill).where(
                Bill.invoice_number == invoice_number
            )
        )

        if bill is None:
            raise BillNotFoundError()

        return bill
    
    def list_bills(
        self,
    ) -> list[Bill]:
        """
        Returns all bills ordered by newest first.
        """

        return self.scalars(
            select(Bill).order_by(
                Bill.created_at.desc()
            )
        )
    
    def cancel_bill(
        self,
        bill_id: int,
    ) -> Bill:
        """
        Cancels a bill and restores inventory.
        """

        bill = self.get_bill(bill_id)

        if bill.payment_status == PaymentStatus.CANCELLED:
            return bill

        try:

            # Restore Inventory

            for item in bill.bill_items:

                self.inventory_service.stock_in(
                    InventoryTransactionCreate(
                        product_id=item.product_id,
                        quantity=item.quantity,
                        transaction_type=InventoryTransactionType.STOCK_IN,
                        remarks=f"Cancelled Invoice {bill.invoice_number}",
                    )
                )

            # Reverse Khata if credit sale

            if (
                bill.payment_method
                == PaymentMethod.CREDIT
                and bill.customer_id
            ):

                self.khata_service.add_payment(
                    KhataTransactionCreate(
                        customer_id=bill.customer_id,
                        amount=bill.grand_total,
                        transaction_type=KhataTransactionType.PAYMENT,
                        remarks=f"Cancelled Invoice {bill.invoice_number}",
                    )
                )

            bill.payment_status = PaymentStatus.CANCELLED

            self.flush()
            self.commit()
            self.refresh(bill)

            return bill

        except Exception:

            self.rollback()
            raise