from uuid import UUID

import aiohttp

from ..config import EVENTS_CAPASHINO_URL, X_API_KEY, PAYMENT_URL
from ..schemas import PaymentCallbackRequest, PaymentCallbackResponse


class PaymentService:
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

    async def create_payment(self, request: PaymentCallbackRequest) -> PaymentCallbackResponse:
        async with self.session.post(
            f"{EVENTS_CAPASHINO_URL}/api/payments",
            json=request.model_dump_json()
        ) as response:
            result = await response.json()
        return result
