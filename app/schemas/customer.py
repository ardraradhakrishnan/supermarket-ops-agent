from pydantic import BaseModel, ConfigDict, EmailStr


class CustomerBase(BaseModel):
    """
    Shared customer fields.
    """

    name: str
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None


class CustomerCreate(CustomerBase):
    """
    Schema for creating a customer.
    """

    pass


class CustomerUpdate(BaseModel):
    """
    Schema for updating a customer.
    """

    name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None


class CustomerResponse(CustomerBase):
    """
    Schema returned to clients.
    """

    id: int

    model_config = ConfigDict(from_attributes=True)