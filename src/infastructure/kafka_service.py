import asyncio
import json
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from ..config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_PRODUCER_TOPIC, KAFKA_CONSUMER_TOPIC

class KafkaProducer:

    async def __aenter__(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
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
        )
        await self.consumer.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.consumer:
            await self.consumer.stop()

    async def get(self):
        messages = []
        async for msg in self.consumer:
            messages.append(msg.value)
        return messages