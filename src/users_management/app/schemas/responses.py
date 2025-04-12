from users_management.core.schemas.base import BaseSchema


class SuccessResponse(BaseSchema):
    """Scheme for a successful response."""

    message: str = "success"


class ErrorResponse(BaseSchema):
    """Error response scheme."""

    error_type: str
    message: str
