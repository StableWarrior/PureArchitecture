from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class OrderRequest(BaseModel):
    user_id: str
    quantity: int
    item_id: UUID
    idempotency_key: Optional[str] = None


class OrderResponse(BaseModel):
    id: UUID
    user_id: str
    quantity: int
    item_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime
