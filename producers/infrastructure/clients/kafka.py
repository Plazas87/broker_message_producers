"""Kafka client module."""
import logging
from dataclasses import dataclass
from typing import Dict

from kafka import KafkaProducer

from ...application.ports import IMessage, IProducer, ISerializer

logger = logging.getLogger(__name__)


@dataclass
class KafkaMessage(IMessage):
    """KafkaMessage DTO."""

    topic: str
    partition: str
    body: bytes


class Producer(IProducer):
    """Kafka Producer class."""

    _serializer: ISerializer[Dict[str, int], bytes]
    _bootstrap_server_host: str
    _bootstrap_server_port: int

    def __init__(
        self,
        serializer: ISerializer[Dict[str, int], bytes],
        bootstrap_server_host: str,
        bootstrap_server_port: int,
    ) -> None:
        self._serializer = serializer
        self._broker_client = KafkaProducer(
            bootstrap_servers=f"{bootstrap_server_host}:{str(bootstrap_server_port)}",
            value_serializer=self._serializer.serialize,
        )

    def publish(self, message: KafkaMessage) -> None:
        """Publish data to the broker."""
        self._broker_client.send(
            topic=message.topic, partition=message.partition, value=message.body
        )
        logger.info("Message sent: '%s'", message.body)
