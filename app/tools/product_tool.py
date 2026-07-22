from app.database.database import SessionLocal

from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
)

from app.services.product_service import ProductService

from app.utils.serializers import (
    serialize_product,
    serialize_products,
)


def search_product(
    keyword: str,
) -> list[dict]:
    """
    Search products by name or SKU.
    """

    db = SessionLocal()

    try:

        service = ProductService(db)

        products = service.search(
            keyword
        )

        return serialize_products(
            products
        )

    finally:

        db.close()

def list_products():
    """
    Returns all products.
    """

    db = SessionLocal()

    try:

        service = ProductService(db)

        products = service.list()

        return serialize_products(
            products
        )

    finally:

        db.close()

def create_product(
    product: ProductCreate,
) -> dict:
    """
    Creates a new product.
    """

    db = SessionLocal()

    try:

        service = ProductService(db)

        new_product = service.create(
            product
        )

        service.commit()

        return serialize_product(
            new_product
        )

    except Exception:

        service.rollback()
        raise

    finally:

        db.close()

def update_product(
    product_id: int,
        product: ProductUpdate,
    ):
    db = SessionLocal()

    try:

        service = ProductService(db)

        updated = service.update(
            product_id,
            product,
        )

        service.commit()

        return serialize_product(
            updated
        )

    except:

        service.rollback()
        raise

    finally:

        db.close()


def deactivate_product(
    product_id: int,
    ):
    db = SessionLocal()

    try:

        service = ProductService(db)

        product = service.deactivate(
            product_id,
        )

        service.commit()

        return serialize_product(
            product
        )

    except:

        service.rollback()
        raise

    finally:

        db.close()