from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class TimestampMixin(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class BaseModel(TimestampMixin):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)


class BaseSQLModel(SQLModel):
    """Base class for all SQLModel classes to inherit from."""
    pass
