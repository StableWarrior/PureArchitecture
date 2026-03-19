from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class OrderRequest(BaseModel):
    user_id: str
    quantity: int
    item_id: UUID
    idempotency_key: Optional[UUID] = None


class OrderResponse(BaseModel):
    id: UUID
    user_id: str
    quantity: int
    item_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime

