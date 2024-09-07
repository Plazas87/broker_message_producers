"""Producers package entrypoint."""
import logging
from typing_extensions import Annotated
import typer

from .infrastructure.clients.kafka import KafkaMessage
from .infrastructure.data_readers.csv import Reader
from .infrastructure import serializers
from .infrastructure import clients


logging.basicConfig(encoding="utf-8", format='%(levelname)s:%(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

app = typer.Typer(rich_markup_mode="rich")


@app.command()
def kafka(
    host: Annotated[
        str, typer.Option(help="Bootstrap server host.")
    ],
    port: Annotated[
        int, typer.Option(help="Bootstrap server port.")
    ],
    topic: Annotated[
        str, typer.Option(help="Topic to publish message to.")
    ],
    partition: Annotated[
        int, typer.Option(help="Topic's partition.")
    ],
    file_path: Annotated[
        str,
        typer.Option(help="Path to the '.csv' file."),
    ] = ".",
) -> None:
    """Publish messages to a kafka broker."""
    reader = Reader(path=file_path)
    producer = clients.kafka.Producer(
        bootstrap_server_host=host, bootstrap_server_port=port, serializer=serializers.bytes.Serializer()
    )

    # start reading the data as a stream
    for data in reader.read():
        message = KafkaMessage(topic=topic, partition=partition, body=data)

        producer.publish(message=message)


@app.command()
def rabbit_mq(
    host: Annotated[
        str, typer.Option(help="Broker server host.")
    ],
    port: Annotated[
        int, typer.Option(help="Broker server port.")
    ],
    exchange: Annotated[
        str, typer.Option(help="Exchange to use.")
    ],
    topic: Annotated[
        str, typer.Option(help="Topic to publish message to.")
    ],
    vhost: Annotated[
        str, typer.Option(help="Virtual host.")
    ],
    user: Annotated[str, typer.Option(
        help="User."
    )],
    password: Annotated[str, typer.Option(
        help="Password."
    )],
    file_path: Annotated[
        str,
        typer.Option(
            help="Path to the '.csv' file that contains the sample data."
        ),
    ] = ".",
) -> None:
    """Plusblish messages to RabbitMQ broker."""
    reader = Reader(path=file_path)
    bytes_seralizar = serializers.bytes.Serializer()

    logger.info("Starting the RabbitMQ producer...")

    producer = clients.rabbitmq.Producer(
        host=host,
        port=port,
        user=user,
        password=password,
        vhost=vhost,
        delivery_mode="Transient",
        content_type="application/json",
        content_encoding="utf-8",
    )

    # Start reading the data as a stream from a file.
    with producer as publisher:
        for data in reader.read():
            message = clients.rabbitmq.RabbitMQMessage(
                topic=topic,
                exchange=exchange,
                body=bytes_seralizar.serialize(data=data)
            )
            publisher.publish(message=message)


if __name__ == "__main__":
    app()
