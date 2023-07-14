"""Kafka client module."""
from typing import Dict
from kafka import KafkaProducer
from ...application.ports import IProducer, IReader, ISerializer


class Producer(IProducer):
    """Producer class."""
    _data_source: IReader[Dict[str, int]]
    _serializer: ISerializer[Dict[str, int], bytes]
    _bootstrap_server_host: str
    _bootstrap_server_port: int
    _topic: str
    _partition: 0

    def __init__(self,
        data_source: IReader[Dict[str, int]],
        serializer: ISerializer[Dict[str, int], bytes],
        bootstrap_server_host: str,
        bootstrap_server_port: int,
        topic: str,
        partition: int
    ) -> None:
        self._data_source = data_source
        self._serializer = serializer
        self._broker_client = KafkaProducer(
            bootstrap_servers=f'{bootstrap_server_host}:{str(bootstrap_server_port)}',
            value_serializer=serializer.serialize
        )
        self._topic = topic
        self._partition = partition

    def publish(self) -> None:
        """Publish data to the broker."""
        # start reading the data as a stream
        for data in self._data_source.read():
            self._broker_client.send(
                topic=self._topic,
                partition=self._partition,
                value=data
            )

