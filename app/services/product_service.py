from __future__ import annotations

from sqlalchemy import or_, select

from app.models.products import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.base_service import BaseService


class ProductService(BaseService):
    """
    Service responsible for all product-related operations.
    """

    def create(self, product: ProductCreate) -> Product:
        """
        Create a new product.
        """

        existing_product = self.scalar(
            select(Product).where(
                Product.sku == product.sku
            )
        )

        if existing_product:
            raise ValueError(
                f"Product with SKU '{product.sku}' already exists."
            )

        db_product = Product(
            **product.model_dump()
        )

        self.add(db_product)
        self.flush()
        self.refresh(db_product)

        return db_product

    def get_by_id(
        self,
        product_id: int,
    ) -> Product | None:
        """
        Returns a product by its ID.
        """

        return self.scalar(
            select(Product).where(
                Product.id == product_id
            )
        )

    def get_by_sku(
        self,
        sku: str,
    ) -> Product | None:
        """
        Returns a product by SKU.
        """

        return self.scalar(
            select(Product).where(
                Product.sku == sku
            )
        )

    def list(
        self,
        active_only: bool = True,
    ) -> list[Product]:
        """
        Returns all products.
        """

        query = select(Product)

        if active_only:
            query = query.where(
                Product.is_active.is_(True)
            )

        return self.scalars(query)

    def search(
        self,
        keyword: str,
    ) -> list[Product]:
        """
        Search products by SKU or name.
        """

        query = (
            select(Product)
            .where(
                or_(
                    Product.name.ilike(f"%{keyword}%"),
                    Product.sku.ilike(f"%{keyword}%"),
                )
            )
            .order_by(Product.name)
        )

        return self.scalars(query)

    def update(
        self,
        product_id: int,
        product_data: ProductUpdate,
    ) -> Product:
        """
        Update an existing product.
        """

        product = self.get_by_id(product_id)

        if product is None:
            raise ValueError(
                "Product not found."
            )

        updates = product_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        if (
            "sku" in updates
            and updates["sku"] != product.sku
        ):
            existing_product = self.scalar(
                select(Product).where(
                    Product.sku == updates["sku"]
                )
            )

            if existing_product:
                raise ValueError(
                    f"Product with SKU '{updates['sku']}' already exists."
                )

        for field, value in updates.items():
            setattr(
                product,
                field,
                value,
            )

        self.flush()
        self.refresh(product)

        return product

    def activate(
        self,
        product_id: int,
    ) -> Product:
        """
        Activate a product.
        """

        product = self.get_by_id(product_id)

        if product is None:
            raise ValueError(
                "Product not found."
            )

        product.is_active = True

        self.flush()
        self.refresh(product)

        return product

    def deactivate(
        self,
        product_id: int,
    ) -> Product:
        """
        Deactivate a product.
        """

        product = self.get_by_id(product_id)

        if product is None:
            raise ValueError(
                "Product not found."
            )

        product.is_active = False

        self.flush()
        self.refresh(product)

        return product

    def exists(
        self,
        sku: str,
    ) -> bool:
        """
        Check whether a product exists.
        """

        return (
            self.scalar(
                select(Product).where(
                    Product.sku == sku
                )
            )
            is not None
        )