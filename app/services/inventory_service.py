from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select

from app.core.exceptions import (
    InsufficientStockError,
    ProductNotFoundError,
)
from app.models.enums import InventoryTransactionType
from app.models.inventory import InventoryTransaction
from app.models.products import Product
from app.schemas.inventory import InventoryTransactionCreate
from app.services.base_service import BaseService
from app.services.preference_service import PreferenceService


class InventoryService(BaseService):
    """
    Handles all inventory operations.
    """

    def _get_product(
        self,
        product_id: int,
    ) -> Product:
        """
        Returns the requested product.
        """

        product = self.scalar(
            select(Product).where(
                Product.id == product_id
            )
        )

        if product is None:
            raise ProductNotFoundError()

        return product

    def record_purchase(
        self,
        transaction: InventoryTransactionCreate,
    ) -> InventoryTransaction:
        """
        Records a purchase transaction.
        """

        self._get_product(
            transaction.product_id
        )

        inventory = InventoryTransaction(
            product_id=transaction.product_id,
            quantity=transaction.quantity,
            reference=transaction.reference,
            remarks=transaction.remarks,
            transaction_type=InventoryTransactionType.PURCHASE,
        )

        self.add(inventory)
        self.flush()
        self.refresh(inventory)

        return inventory

    def record_sale(
        self,
        transaction: InventoryTransactionCreate,
    ) -> InventoryTransaction:
        """
        Records a sale transaction.
        """

        self._get_product(
            transaction.product_id
        )

        if not self.has_stock(
            transaction.product_id,
            transaction.quantity,
        ):
            raise InsufficientStockError()

        inventory = InventoryTransaction(
            product_id=transaction.product_id,
            quantity=transaction.quantity,
            reference=transaction.reference,
            remarks=transaction.remarks,
            transaction_type=InventoryTransactionType.SALE,
        )

        self.add(inventory)
        self.flush()
        self.refresh(inventory)

        return inventory

    def record_return(
        self,
        transaction: InventoryTransactionCreate,
    ) -> InventoryTransaction:
        """
        Records a customer return.
        """

        self._get_product(
            transaction.product_id
        )

        inventory = InventoryTransaction(
            product_id=transaction.product_id,
            quantity=transaction.quantity,
            reference=transaction.reference,
            remarks=transaction.remarks,
            transaction_type=InventoryTransactionType.RETURN,
        )

        self.add(inventory)
        self.flush()
        self.refresh(inventory)

        return inventory

    def record_damage(
        self,
        transaction: InventoryTransactionCreate,
    ) -> InventoryTransaction:
        """
        Records damaged inventory.
        """

        self._get_product(
            transaction.product_id
        )

        if not self.has_stock(
            transaction.product_id,
            transaction.quantity,
        ):
            raise InsufficientStockError()

        inventory = InventoryTransaction(
            product_id=transaction.product_id,
            quantity=transaction.quantity,
            reference=transaction.reference,
            remarks=transaction.remarks,
            transaction_type=InventoryTransactionType.DAMAGE,
        )

        self.add(inventory)
        self.flush()
        self.refresh(inventory)

        return inventory

    def get_current_stock(
        self,
        product_id: int,
    ) -> Decimal:
        """
        Calculates current stock.
        """

        self._get_product(product_id)

        transactions = self.scalars(
            select(
                InventoryTransaction
            ).where(
                InventoryTransaction.product_id
                == product_id
            )
        )

        stock = Decimal("0")

        for tx in transactions:

            if tx.transaction_type in (
                InventoryTransactionType.PURCHASE,
                InventoryTransactionType.RETURN,
            ):
                stock += tx.quantity

            elif tx.transaction_type in (
                InventoryTransactionType.SALE,
                InventoryTransactionType.DAMAGE,
            ):
                stock -= tx.quantity

            elif (
                tx.transaction_type
                == InventoryTransactionType.ADJUSTMENT
            ):
                stock += tx.quantity

        return stock

    def has_stock(
        self,
        product_id: int,
        quantity: Decimal,
    ) -> bool:
        """
        Returns whether sufficient stock exists.
        """

        return (
            self.get_current_stock(product_id)
            >= quantity
        )

    def get_stock_history(
        self,
        product_id: int,
    ) -> list[InventoryTransaction]:
        """
        Returns inventory history.
        """

        self._get_product(product_id)

        return self.scalars(
            select(
                InventoryTransaction
            )
            .where(
                InventoryTransaction.product_id
                == product_id
            )
            .order_by(
                InventoryTransaction.created_at.desc()
            )
        )

    def get_low_stock_products(
        self,
    ) -> list[dict]:
        """
        Returns all low-stock products.
        """

        preference_service = PreferenceService(
            self.db
        )

        threshold = (
            preference_service.get_low_stock_threshold()
        )

        products = self.scalars(
            select(Product).where(
                Product.is_active.is_(True)
            )
        )

        result = []

        for product in products:

            stock = self.get_current_stock(
                product.id
            )

            if stock <= threshold:

                result.append(
                    {
                        "product": product,
                        "stock": stock,
                    }
                )

        return result

    def adjust_stock(
        self,
        product_id: int,
        new_quantity: Decimal,
    ) -> InventoryTransaction:
        """
        Adjusts inventory to the desired quantity.
        """

        self._get_product(product_id)

        current = self.get_current_stock(
            product_id
        )

        difference = (
            new_quantity - current
        )

        if difference == 0:
            raise ValueError(
                "Stock is already up to date."
            )

        inventory = InventoryTransaction(
            product_id=product_id,
            quantity=difference,
            transaction_type=InventoryTransactionType.ADJUSTMENT,
            remarks="Manual stock adjustment",
        )

        self.add(inventory)
        self.flush()
        self.refresh(inventory)

        return inventory
