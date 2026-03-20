from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import OrderRequest

from ..models import Order


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, order: OrderRequest) -> Order:

        order_data = order.model_dump()
        order = Order(**order_data)

        self.db.add(order)
        await self.db.flush()

        return order

    async def get_order(
        self, order_id: UUID | None = None, idempotency_key: str | None = None
    ) -> Order | None:

        if idempotency_key is None:
            result = await self.db.execute(select(Order).where(Order.id == order_id))
        else:
            result = await self.db.execute(
                select(Order).where(Order.idempotency_key == idempotency_key)
            )

        order = result.scalar_one_or_none()

        return order

    async def update_order(self, order_id: UUID, status: str) -> Order | None:

        result = await self.db.execute(
            update(Order)
            .where(Order.id == order_id, Order.status != status)
            .values(status=status)
            .returning(Order)
        )
        order = result.scalar_one_or_none()

        return order
