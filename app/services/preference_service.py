from sqlalchemy import select

from app.models.preference import Preference
from app.services.base_service import BaseService


class PreferenceService(BaseService):
    """
    Handles application preferences.
    """

    def get(self, key: str) -> str | None:
        """
        Returns the value for the given preference key.
        """

        preference = self.scalar(
            select(Preference).where(
                Preference.key == key
            )
        )

        if preference is None:
            return None

        return preference.value

    def set(self, key: str, value: str) -> Preference:
        """
        Creates or updates a preference.
        """

        preference = self.scalar(
            select(Preference).where(
                Preference.key == key
            )
        )

        if preference is None:
            preference = Preference(
                key=key,
                value=value,
            )

            self.add(preference)

        else:
            preference.value = value

        self.flush()
        self.refresh(preference)

        return preference

    def get_store_name(self) -> str:
        """
        Returns the configured store name.
        """

        return self.get("store_name") or "Supermarket"

    def get_currency(self) -> str:
        """
        Returns the configured currency.
        """

        return self.get("currency") or "INR"

    def get_low_stock_threshold(self) -> int:
        """
        Returns the configured low stock threshold.
        """

        value = self.get("low_stock_threshold")

        if value is None:
            return 10

        return int(value)