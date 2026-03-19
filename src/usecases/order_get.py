from ..schemas import OrderRequest
from fastapi import HTTPException
from uuid import UUID
from ..database.models import Order
from ..infastructure.session import Session
from ..database.connection import async_session


class OrderGetUseCase:

    @classmethod
    async def get_order(cls, order_id: UUID) -> Order:
        async with Session(async_session()) as db:
            result = await db.orders.get_order(order_id=order_id)
            if result is None:
                raise HTTPException(status_code=404, detail="Order not found")
            return result
