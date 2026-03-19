from uuid import UUID

import aiohttp

from ..config import EVENTS_CAPASHINO_URL, X_API_KEY


class CatalogService:
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "x-api-key": X_API_KEY,
                "Content-Type": "application/json",
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_item(self, item_id: UUID) -> dict:
        async with self.session.get(
            f"{EVENTS_CAPASHINO_URL}/api/catalog/items/{item_id}"
        ) as response:
            result = await response.json()
        return result
