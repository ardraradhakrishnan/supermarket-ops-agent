from datetime import date
from decimal import Decimal

from sqlalchemy import func, select

from app.models.billing import Bill, BillItem
from app.models.customer import Customer
from app.models.products import Product

from app.services.base_service import BaseService
from app.services.inventory_service import InventoryService
from app.services.khata_service import KhataService


class AnalyticsService(BaseService):
    """
    Provides business reports and dashboard analytics.
    """

    def get_dashboard_summary(self) -> dict:
        """
        Returns overall dashboard statistics.
        """

        total_products = self.scalar(
            select(func.count(Product.id))
        )

        total_customers = self.scalar(
            select(func.count(Customer.id))
        )

        today = date.today()

        today_sales = self.scalar(
            select(
                func.coalesce(
                    func.sum(Bill.total_amount),
                    0,
                )
            ).where(
                func.date(Bill.created_at) == today
            )
        )

        today_bills = self.scalar(
            select(
                func.count(Bill.id)
            ).where(
                func.date(Bill.created_at) == today
            )
        )

        inventory_service = InventoryService(self.db)

        low_stock_products = len(
            inventory_service.get_low_stock_products()
        )

        khata_service = KhataService(self.db)

        pending_khata = Decimal("0")

        customers = self.scalars(
            select(Customer)
        )

        for customer in customers:

            pending_khata += (
                khata_service.get_balance(customer.id)
            )

        return {
            "total_products": total_products,
            "total_customers": total_customers,
            "today_sales": today_sales,
            "today_bills": today_bills,
            "low_stock_products": low_stock_products,
            "pending_khata": pending_khata,
        }

    def get_sales_summary(self) -> dict:
        """
        Returns today's sales summary.
        """

        today = date.today()

        total_sales = self.scalar(
            select(
                func.coalesce(
                    func.sum(Bill.total_amount),
                    0,
                )
            ).where(
                func.date(Bill.created_at) == today
            )
        )

        bill_count = self.scalar(
            select(
                func.count(Bill.id)
            ).where(
                func.date(Bill.created_at) == today
            )
        )

        average_bill = (
            Decimal(total_sales) / bill_count
            if bill_count
            else Decimal("0")
        )

        return {
            "sales_amount": total_sales,
            "bill_count": bill_count,
            "average_bill": average_bill,
        }

    def get_top_selling_products(
        self,
        limit: int = 10,
    ) -> list[dict]:
        """
        Returns best selling products.
        """

        rows = self.execute(
            select(
                Product.name,
                func.sum(BillItem.quantity).label(
                    "quantity"
                ),
            )
            .join(
                BillItem,
                Product.id == BillItem.product_id,
            )
            .group_by(Product.id)
            .order_by(
                func.sum(
                    BillItem.quantity
                ).desc()
            )
            .limit(limit)
        )

        return [
            {
                "product": row.name,
                "quantity": row.quantity,
            }
            for row in rows
        ]

    def get_low_stock_report(
        self,
    ) -> list[dict]:
        """
        Returns products below threshold.
        """

        inventory = InventoryService(self.db)

        products = inventory.get_low_stock_products()

        return [
            {
                "product": item["product"].name,
                "stock": item["stock"],
            }
            for item in products
        ]

    def get_customer_outstanding_report(
        self,
    ) -> list[dict]:
        """
        Returns customers having pending Khata.
        """

        khata = KhataService(self.db)

        customers = self.scalars(
            select(Customer)
        )

        result = []

        for customer in customers:

            balance = khata.get_balance(
                customer.id
            )

            if balance > 0:

                result.append(
                    {
                        "customer": customer.name,
                        "balance": balance,
                    }
                )

        return result

    def get_inventory_value(self) -> dict:
        """
        Returns total inventory value.
        """

        inventory = InventoryService(self.db)

        total = Decimal("0")

        products = self.scalars(
            select(Product)
        )

        for product in products:

            stock = inventory.get_current_stock(
                product.id
            )

            total += (
                stock * product.selling_price
            )

        return {
            "inventory_value": total
        }

    def get_recent_sales(
        self,
        limit: int = 10,
    ) -> list[dict]:
        """
        Returns recently created bills.
        """

        bills = self.scalars(
            select(Bill)
            .order_by(
                Bill.created_at.desc()
            )
            .limit(limit)
        )

        return [
            {
                "bill_id": bill.id,
                "customer_id": bill.customer_id,
                "amount": bill.total_amount,
                "created_at": bill.created_at,
            }
            for bill in bills
        ]
