from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..models import Outbox


class OutboxRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(
        self, event_type: str, payload: dict[str, Any], status: str, order_id: UUID
    ):

        outbox = Outbox(
            event_type=event_type,
            payload=payload,
            status=status,
            order_id=order_id,
        )
        self.db.add(outbox)

        return outbox

    async def get(self, status: str, event_type: str | None):
        filters = [Outbox.status == status]
        if event_type:
            filters.append(Outbox.event_type == event_type)

        result = await self.db.execute(
            select(Outbox).options(joinedload(Outbox.order)).where(*filters)
        )

        outboxes = result.unique().scalars().all()

        return outboxes

    async def update(self, outbox: Outbox):
        outbox.status = "отправлено"
        await self.db.flush()

        return outbox
