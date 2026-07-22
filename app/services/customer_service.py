from sqlalchemy import or_, select

from app.core.exceptions import (
    CustomerNotFoundError,
    DuplicateCustomerError,
)
from app.models.customer import Customer
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
)
from app.services.base_service import BaseService


class CustomerService(BaseService):
    """
    Service responsible for customer-related operations.
    """

    def create(
        self,
        customer: CustomerCreate,
    ) -> Customer:
        """
        Creates a new customer.
        """

        if customer.phone:

            existing = self.scalar(
                select(Customer).where(
                    Customer.phone == customer.phone
                )
            )

            if existing:
                raise DuplicateCustomerError(
                    f"Customer with phone '{customer.phone}' already exists."
                )

        db_customer = Customer(
            **customer.model_dump()
        )

        self.add(db_customer)
        self.flush()
        self.refresh(db_customer)

        return db_customer

    def get(
        self,
        customer_id: int,
    ) -> Customer:
        """
        Returns a customer by id.
        """

        customer = self.scalar(
            select(Customer).where(
                Customer.id == customer_id
            )
        )

        if customer is None:
            raise CustomerNotFoundError()

        return customer

    def get_by_phone(
        self,
        phone: str,
    ) -> Customer | None:
        """
        Returns a customer by phone number.
        """

        return self.scalar(
            select(Customer).where(
                Customer.phone == phone
            )
        )

    def get_walkin_customer(
        self,
    ) -> Customer:
        """
        Returns the default walk-in customer.
        """

        customer = self.scalar(
            select(Customer).where(
                Customer.name == "Walk-in Customer"
            )
        )

        if customer is None:
            raise CustomerNotFoundError(
                "Walk-in customer not found."
            )

        return customer

    def list(
        self,
    ) -> list[Customer]:
        """
        Returns all active customers.
        """

        return self.scalars(
            select(Customer)
            .where(
                Customer.is_active.is_(True)
            )
            .order_by(Customer.name)
        )

    def search(
        self,
        keyword: str,
    ) -> list[Customer]:
        """
        Search customers by name, phone or email.
        """

        query = (
            select(Customer)
            .where(
                Customer.is_active.is_(True),
                or_(
                    Customer.name.ilike(
                        f"%{keyword}%"
                    ),
                    Customer.phone.ilike(
                        f"%{keyword}%"
                    ),
                    Customer.email.ilike(
                        f"%{keyword}%"
                    ),
                ),
            )
            .order_by(
                Customer.name
            )
        )

        return self.scalars(query)

    def update(
        self,
        customer_id: int,
        customer_data: CustomerUpdate,
    ) -> Customer:
        """
        Updates a customer.
        """

        customer = self.get(
            customer_id
        )

        updates = customer_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        if (
            "phone" in updates
            and updates["phone"] != customer.phone
        ):

            existing = self.scalar(
                select(Customer).where(
                    Customer.phone == updates["phone"]
                )
            )

            if (
                existing
                and existing.id != customer.id
            ):
                raise DuplicateCustomerError(
                    f"Customer with phone '{updates['phone']}' already exists."
                )

        for field, value in updates.items():

            setattr(
                customer,
                field,
                value,
            )

        self.flush()
        self.refresh(customer)

        return customer

    def deactivate(
        self,
        customer_id: int,
    ) -> Customer:
        """
        Soft deletes a customer.
        """

        customer = self.get(
            customer_id
        )

        customer.is_active = False

        self.flush()
        self.refresh(customer)

        return customer

    def exists(
        self,
        customer_id: int,
    ) -> bool:
        """
        Returns whether a customer exists.
        """

        return (
            self.scalar(
                select(Customer.id).where(
                    Customer.id == customer_id
                )
            )
            is not None
        )