from sqlalchemy.ext.asyncio import AsyncSession

from ..database.repository.inbox_repository import InboxRepository
from ..database.repository.order_repository import OrderRepository
from ..database.repository.outbox_repository import OutboxRepository


class Session:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.order_repo = OrderRepository(session)
        self.outbox_repo = OutboxRepository(session)
        self.inbox_repo = InboxRepository(session)

    async def __aenter__(self):
        await self.session.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            try:
                await self.commit()
            except Exception:
                await self.rollback()
                raise
        else:
            await self.rollback()

        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    @property
    def orders(self) -> OrderRepository:
        """Доступ к OrderRepository"""
        return self.order_repo

    @property
    def outbox(self) -> OutboxRepository:
        """Доступ к OutboxRepository"""
        return self.outbox_repo

    @property
    def inbox(self) -> InboxRepository:
        """Доступ к InboxRepository"""
        return self.inbox_repo
