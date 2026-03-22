from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Inbox


class InboxRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, event_type: str, payload: dict[str, Any], status: str):

        inbox = Inbox(
            event_type=event_type,
            payload=payload,
            status=status,
        )
        self.db.add(inbox)

        return inbox

    async def get(self, status: str):
        result = await self.db.execute(select(Inbox).where(Inbox.status == status))

        inboxes = result.scalars().all()

        return inboxes
