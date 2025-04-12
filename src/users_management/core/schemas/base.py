from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Basic scheme with general settings."""

    model_config = ConfigDict(strict=True)
