from fastapi import HTTPException

from ..config import PAYMENT_URL
from ..database.connection import async_session
from ..database.models import Order
from ..infastructure.catalog_service import CatalogService
from ..infastructure.payment_service import PaymentService
from ..infastructure.session import Session
from ..schemas import OrderRequest, PaymentCallbackRequest


class OrderCreateUseCase:
    @classmethod
    async def create_order(cls, order: OrderRequest) -> Order:
        # Проверяем что кол-ва достаточно
        async with CatalogService() as catalog:
            result = await catalog.get_item(item_id=order.item_id)
        if result["available_qty"] < order.quantity:
            raise HTTPException(status_code=400, detail="Order out of stock")

        async with Session(async_session()) as db:
            # Проверяем та же это операция или нет, если заказ такой есть, возвращаем его
            result = await db.orders.get_order(idempotency_key=order.idempotency_key)
            if result:
                return result
            # Иначе создаем новый заказ
            result = await db.orders.create_order(order=order)

            await db.outbox.save(
                event_type="order.new",
                payload={},
                status="ожидает отправки",
                order_id=result.id,
            )

        # Создаем платеж
        async with PaymentService() as payment:
            request = PaymentCallbackRequest(
                order_id=result.id,
                amount=str(result.quantity),
                callback_url=f"{PAYMENT_URL}/api/orders/payment-callback",
                idempotency_key=result.idempotency_key,
            )
            await payment.create_payment(request=request)

        return result
