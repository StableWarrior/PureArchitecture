import json

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from ..config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_CONSUMER_TOPIC,
    KAFKA_PRODUCER_TOPIC,
)


class KafkaProducer:
    async def __aenter__(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await self.producer.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.producer:
            await self.producer.stop()

    async def send(self, event: dict):
        await self.producer.send_and_wait(KAFKA_PRODUCER_TOPIC, event)


class KafkaConsumer:
    async def __aenter__(self):
        self.consumer = AIOKafkaConsumer(
            KAFKA_CONSUMER_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
        )
        await self.consumer.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.consumer:
            await self.consumer.stop()

    async def get(self):
        messages = []
        batch = await self.consumer.getmany(timeout_ms=10000, max_records=5)
        for tp, msgs in batch.items():
            for msg in msgs:
                messages.append(msg.value)
        return messages
