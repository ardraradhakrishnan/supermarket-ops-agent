from pydantic import BaseModel, ConfigDict


class PreferenceBase(BaseModel):
    """
    Shared preference fields.
    """

    key: str
    value: str
    description: str | None = None


class PreferenceCreate(PreferenceBase):
    """
    Schema for creating preferences.
    """

    pass


class PreferenceUpdate(BaseModel):
    """
    Schema for updating preferences.
    """

    value: str
    description: str | None = None


class PreferenceResponse(PreferenceBase):
    """
    Schema returned to clients.
    """

    id: int

    model_config = ConfigDict(from_attributes=True)