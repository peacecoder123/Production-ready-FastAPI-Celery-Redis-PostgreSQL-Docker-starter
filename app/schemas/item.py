from __future__ import annotations

import datetime

from pydantic import BaseModel, ConfigDict, Field


class ItemCreate(BaseModel):
    """Payload for creating a new item."""

    name: str = Field(..., min_length=1, max_length=255, examples=["My Item"])
    description: str | None = Field(None, examples=["A short description"])


class ItemRead(BaseModel):
    """Public representation of an item."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    created_at: datetime.datetime
