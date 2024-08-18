"""RabbitMQ producer module."""
from __future__ import annotations
from dataclasses import dataclass

import logging

import pika
from pika.adapters.blocking_connection import BlockingChannel

from ...application.ports import IProducer, IMessage

logger = logging.getLogger(__name__)


@dataclass
class RabbitMQMessage(IMessage):
    """RabbitMQMessage class."""

    exchange: str
    topic: str
    body: bytes

 
class Producer(IProducer[IMessage]):
    """RabbitMQ Producer class."""

    _user: str
    _password: str
    _host: str
    _port: str
    _vhost: str
    _delivery_mode: str
    _content_type: str
    _content_encoding: str
    _channel: BlockingChannel

    def __init__(
        self,
        user: str,
        password: str,
        host: str,
        port: str,
        vhost: str,
        delivery_mode: str = "Persistant",
        content_type: str = "application/json",
        content_encoding: str = "utf-8"
    ) -> None:
        """Class constructor."""
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._vhost = vhost
        self._connection = None
        self._delivery_mode = delivery_mode
        self._content_type = content_type
        self._content_encoding = content_encoding

    def _connect(self) -> None:
        """Connect to RabbitMQ."""
        credentials = pika.PlainCredentials(self._user, self._password)
        parameters = pika.ConnectionParameters(
            host=self._host, port=self._port, virtual_host=self._vhost, credentials=credentials
        )
        self._connection = pika.BlockingConnection(parameters=parameters)

    def __enter__(self) -> Producer:
        """Create and start a connection with rabbitmq using the context manager interface."""
        self._connect()
        self._channel = self._connection.channel()

        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Stop the connection when the context manager is exited."""
        # Gracefully close the connection
        self._connection.close()

    def publish(self, message: RabbitMQMessage) -> None:
        """
        Publish a message to RabbitMQ.

        Args:
            message (RabbitMQMessage): message to publish

        Returns
            None 
        """
        properties = pika.BasicProperties(
            delivery_mode=pika.DeliveryMode[self._delivery_mode],
            content_type=self._content_type,
            content_encoding=self._content_encoding
        )

        self._channel.basic_publish(
            exchange=message.exchange,
            routing_key=message.topic,
            body=message.body,
            properties=properties
        )
        logger.info("Message sent: '%s'", message.body)

