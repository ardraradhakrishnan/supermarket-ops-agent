from __future__ import annotations

from decimal import Decimal

from sqlalchemy import func, select, or_, desc

from app.core.exceptions import CustomerNotFoundError
from app.models.customer import Customer
from app.models.khata import KhataTransaction
from app.models.enums import KhataTransactionType
from app.schemas.khata import KhataTransactionCreate
from app.services.base_service import BaseService


class KhataService(BaseService):
    """
    Handles customer credit (Khata) operations.
    """

    def _calculate_balance_after(
        self,
        customer_id: int,
        transaction_type: KhataTransactionType,
        amount: Decimal,
    ) -> Decimal:
        """
        Calculates the balance_after value for a new transaction.
        """

        current_balance = self.get_balance(customer_id)

        if transaction_type == KhataTransactionType.CREDIT:
            return current_balance + amount
        else:
            return current_balance - amount

    def add_credit(
        self,
        transaction: KhataTransactionCreate,
    ) -> KhataTransaction:
        """
        Records a credit transaction.
        """

        customer = self.scalar(
            select(Customer).where(
                Customer.id == transaction.customer_id
            )
        )

        if customer is None:
            raise CustomerNotFoundError()

        balance_after = self._calculate_balance_after(
            transaction.customer_id,
            KhataTransactionType.CREDIT,
            transaction.amount,
        )

        khata = KhataTransaction(
            customer_id=transaction.customer_id,
            transaction_type=transaction.transaction_type,
            amount=transaction.amount,
            remarks=transaction.remarks,
            balance_after=balance_after,
        )

        self.add(khata)
        self.flush()
        self.refresh(khata)

        return khata
    

    def add_payment(
        self,
        transaction: KhataTransactionCreate,
    ) -> KhataTransaction:
        """
        Records a payment against outstanding balance.
        """

        customer = self.scalar(
            select(Customer).where(
                Customer.id == transaction.customer_id
            )
        )

        if customer is None:
            raise CustomerNotFoundError()

        balance_after = self._calculate_balance_after(
            transaction.customer_id,
            KhataTransactionType.DEBIT,
            transaction.amount,
        )

        khata = KhataTransaction(
            customer_id=transaction.customer_id,
            transaction_type=transaction.transaction_type,
            amount=transaction.amount,
            remarks=transaction.remarks,
            balance_after=balance_after,
        )

        self.add(khata)
        self.flush()
        self.refresh(khata)

        return khata
    
    def get_balance(
        self,
        customer_id: int,
    ) -> Decimal:
        """
        Returns the outstanding balance for a customer.
        """

        credit = self.scalar(
            select(
                func.coalesce(
                    func.sum(KhataTransaction.amount),
                    0,
                )
            ).where(
                KhataTransaction.customer_id == customer_id,
                KhataTransaction.transaction_type
                == KhataTransactionType.CREDIT,
            )
        )

        payment = self.scalar(
            select(
                func.coalesce(
                    func.sum(KhataTransaction.amount),
                    0,
                )
            ).where(
                KhataTransaction.customer_id == customer_id,
                KhataTransaction.transaction_type
                == KhataTransactionType.DEBIT,
            )
        )

        return Decimal(credit) - Decimal(payment)
    
    def get_ledger(
        self,
        customer_id: int,
    ) -> list[KhataTransaction]:
        """
        Returns all Khata transactions for a customer.
        """

        return self.scalars(
            select(KhataTransaction)
            .where(
                KhataTransaction.customer_id == customer_id
            )
            .order_by(
                KhataTransaction.created_at.desc()
            )
        )
    
    def clear_balance(
        self,
        customer_id: int,
    ) -> KhataTransaction | None:
        """
        Clears the customer's outstanding balance by
        creating a payment transaction.
        """

        balance = self.get_balance(customer_id)

        if balance <= 0:
            return None

        payment = KhataTransactionCreate(
            customer_id=customer_id,
            amount=balance,
            transaction_type=KhataTransactionType.DEBIT,
            remarks="Outstanding balance cleared",
        )

        return self.add_payment(payment)

    def search_customer_ledger(
        self,
        keyword: str,
    ) -> list[Customer]:
        """
        Search customers having Khata by
        name or phone.
        """

        query = (
            select(Customer)
            .join(
                KhataTransaction,
                Customer.id == KhataTransaction.customer_id,
            )
            .where(
                or_(
                    Customer.name.ilike(f"%{keyword}%"),
                    Customer.phone.ilike(f"%{keyword}%"),
                )
            )
            .distinct()
            .order_by(Customer.name)
        )

        return self.scalars(query)

    def list_pending_customers(
        self,
    ) -> list[dict]:
        """
        Returns customers having outstanding balance.
        """

        customers = self.scalars(
            select(Customer)
            .order_by(Customer.name)
        )

        result = []

        for customer in customers:

            balance = self.get_balance(customer.id)

            if balance > 0:

                result.append(
                    {
                        "customer": customer,
                        "balance": balance,
                    }
                )

        return result

    def get_total_outstanding(
        self,
    ) -> Decimal:
        """
        Returns total outstanding
        across all customers.
        """

        pending = self.list_pending_customers()

        total = Decimal("0")

        for item in pending:
            total += item["balance"]

        return total

    def get_top_debtors(
        self,
        limit: int = 10,
    ) -> list[dict]:
        """
        Returns customers with
        highest outstanding balance.
        """

        pending = self.list_pending_customers()

        pending.sort(
            key=lambda x: x["balance"],
            reverse=True,
        )

        return pending[:limit]