from uuid import UUID

import aiohttp

from ..config import EVENTS_CAPASHINO_URL, X_API_KEY

class CapashinoService:
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

    async def send(
            self,
            message: str,
            reference_id: UUID,
            idempotency_key: str = None,
    ):
        data = {"message": message, "reference_id": str(reference_id)}
        if idempotency_key:
            data["idempotency_key"] = idempotency_key

        async with self.session.post(
                f"{EVENTS_CAPASHINO_URL}/api/notifications", json=data
        ) as response:
            result = await response.json()

        return result