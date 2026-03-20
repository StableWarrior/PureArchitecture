from datetime import datetime
from typing import Literal, Optional
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


class PaymentCallbackRequest(BaseModel):
    order_id: UUID
    amount: str
    callback_url: str
    idempotency_key: str


class PaymentCallbackResponse(BaseModel):
    payment_id: UUID
    order_id: UUID
    status: Literal["succeeded", "failed"]
    amount: str
    error_message: str | None
