from ..config import LOGGER
from ..database.connection import async_session
from ..infastructure.kafka_service import KafkaConsumer, KafkaProducer
from ..infastructure.session import Session


async def sync_order_paid():
    async with Session(async_session()) as db:
        outboxes = await db.outbox.get(
            event_type="order.paid", status="ожидает отправки"
        )

        for outbox in outboxes:
            try:
                async with KafkaProducer() as kafka:
                    await kafka.send(
                        event={
                            "event_type": outbox.event_type,
                            "order_id": str(outbox.order_id),
                            "item_id": str(outbox.order.item_id),
                            "quantity": outbox.order.quantity,
                            "idempotency_key": outbox.order.idempotency_key,
                        }
                    )
            except Exception as exc:
                error = {
                    "result": False,
                    "error_type": exc.__class__.__name__,
                    "error_message": exc.__str__(),
                }
                LOGGER.error("Failed to sync outbox message", error=error)

            await db.outbox.update(outbox)


async def sync_shipment_status():

    try:
        async with KafkaConsumer() as kafka:
            inboxes = await kafka.get()
    except Exception as exc:
        error = {
            "result": False,
            "error_type": exc.__class__.__name__,
            "error_message": exc.__str__(),
        }
        LOGGER.error("Failed to sync outbox message", error=error)
    LOGGER.info("len", len=inboxes)
    async with Session(async_session()) as db:
        for inbox in inboxes:
            LOGGER.info("inbox", inbox=inbox)
            await db.inbox.save(
                event_type=inbox["event_type"],
                payload=inbox,
                status="ожидает отправки",
            )
            if inbox["event_type"] == "order.shipped":
                await db.orders.update_order(
                    order_id=inbox["order_id"], status="SHIPPED"
                )
            elif inbox["event_type"] == "order.cancelled":
                await db.orders.update_order(
                    order_id=inbox["order_id"], status="CANCELLED"
                )
        inboxes = await db.inbox.get("ожидает отправки")
        LOGGER.info("inboxes", len=len(inboxes))
        LOGGER.info("inboxes", inboxes=inboxes)
