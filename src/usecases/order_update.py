from ..database.connection import async_session
from ..database.models import Order
from ..infastructure.session import Session
from ..schemas import PaymentCallbackResponse


class OrderUpdateUseCase:
    @classmethod
    async def update_order(cls, payment: PaymentCallbackResponse) -> Order:
        async with Session(async_session()) as db:
            payment_data = payment.model_dump()

            if payment_data["status"] == "succeeded":
                result = await db.orders.update_order(
                    order_id=payment_data["order_id"], status="PAID"
                )
            elif payment_data["status"] == "failed":
                result = await db.orders.update_order(
                    order_id=payment_data["order_id"], status="CANCELLED"
                )

            return result
