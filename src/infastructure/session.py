from sqlalchemy.ext.asyncio import AsyncSession

from ..database.repository.order_repository import OrderRepository


class Session:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.order_repo = OrderRepository(session)

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
