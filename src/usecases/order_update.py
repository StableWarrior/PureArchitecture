from ..config import LOGGER
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
                status = "PAID"
                result = await db.orders.update_order(
                    order_id=payment_data["order_id"], status=status
                )
            elif payment_data["status"] == "failed":
                status = "CANCELLED"
                result = await db.orders.update_order(
                    order_id=payment_data["order_id"], status=status
                )

            LOGGER.info("payment", status=status)
            await db.outbox.save(
                event_type=f"order.{status.lower()}",
                payload={},
                status="ожидает отправки",
                order_id=payment_data["order_id"],
            )

            return result
