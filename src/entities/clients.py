from typing import Callable
from aio_pika import connect_robust, DeliveryMode, Message, ExchangeType
import asyncio


class RabbitMQClient:

    def __init__(self, host: str = 'localhost', port: int = 5672, login: str | None = "guest",
                 password: str | None = "guest"):
        self._password = password
        self._login = login
        self._port = port
        self._host = host
        self._connection = None
        self._channel = None

    async def _create_connection(self):
        self._connection = await connect_robust(
            host=self._host,
            port=self._port,
            login=self._login,
            password=self._password
        )
        return self._connection

    async def _create_channel(self):
        connection = await self._create_connection()
        return await connection.channel()


class Publisher(RabbitMQClient):

    def __init__(self, host: str = 'localhost', port: int = 5672, login: str | None = "guest",
                 password: str | None = "guest"):
        super().__init__(host, port, login, password)

    async def publish(self, exchange: str, routing_key: str, body: bytes):
        if not self._channel:
            self._channel = await self._create_channel()

        async with self._channel as channel:
            message = Message(body, delivery_mode=DeliveryMode.PERSISTENT)

            exchange = await channel.declare_exchange(exchange, type=ExchangeType.DIRECT)
            await exchange.publish(message, routing_key=routing_key)


class Consumer(RabbitMQClient):

    def __init__(self, host: str = 'localhost', port: int = 5672, login: str | None = "guest",
                 password: str | None = "guest"):
        super().__init__(host, port, login, password)

    async def consume(self, exchange: str, routing_key: str, callback: Callable):
        if not self._channel:
            self._channel = await self._create_channel()

        async with self._channel as channel:

            queue = await channel.declare_queue(routing_key, durable=True)
            exchange = await channel.declare_exchange(exchange, type=ExchangeType.DIRECT)

            await queue.bind(exchange=exchange, routing_key=routing_key)
            await queue.consume(callback)
            await asyncio.Future()
