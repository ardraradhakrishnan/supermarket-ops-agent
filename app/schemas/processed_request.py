from pydantic import BaseModel, ConfigDict

from app.models.enums import RequestStatus


class ProcessedRequestBase(BaseModel):
    """
    Shared processed request fields.
    """

    request_id: str
    request_text: str
    status: RequestStatus


class ProcessedRequestCreate(ProcessedRequestBase):
    """
    Schema for logging processed requests.
    """

    pass


class ProcessedRequestUpdate(BaseModel):
    """
    Schema for updating request status.
    """

    status: RequestStatus


class ProcessedRequestResponse(ProcessedRequestBase):
    """
    Schema returned to clients.
    """

    id: int

    model_config = ConfigDict(from_attributes=True)