"""Producers package entrypoint."""
import logging
from typing_extensions import Annotated
import typer

from .infrastructure.clients.kafka import KafkaMessage
from .infrastructure.data_readers.csv import Reader
from .infrastructure import serializers
from .infrastructure import clients


logging.basicConfig(encoding="utf-8", level=logging.INFO)


app = typer.Typer(rich_markup_mode="rich")


@app.command()
def kafka(
    host: Annotated[
        str, typer.Option(help="Bootstrap server host.", rich_help_panel="Customization and Utils")
    ],
    port: Annotated[
        int, typer.Option(help="Bootstrap server port.", rich_help_panel="Customization and Utils")
    ],
    topic: Annotated[
        str, typer.Option(help="Topic to publish message to.", rich_help_panel="Customization and Utils")
    ],
    partition: Annotated[
        int, typer.Option(help="Topic's partition.", rich_help_panel="Customization and Utils")
    ],
    file_path: Annotated[
        str,
        typer.Option(
            help="Path to the '.csv' file.",
            rich_help_panel="Customization and Utils",
        ),
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
        str, typer.Option(help="Broker server host.", rich_help_panel="Customization and Utils")
    ],
    port: Annotated[
        int, typer.Option(help="Broker server port.", rich_help_panel="Customization and Utils")
    ],
    exchange: Annotated[
        str, typer.Option(help="Exchange to use.", rich_help_panel="Customization and Utils")
    ],
    topic: Annotated[
        str, typer.Option(help="Topic to publish message to.", rich_help_panel="Customization and Utils")
    ],
    vhost: Annotated[
        str, typer.Option(help="Topic to publish message to.", rich_help_panel="Customization and Utils")
    ],
    user: Annotated[str, typer.Option(
        help="RabbitMQ user.", rich_help_panel="Customization and Utils"
    )],
    password: Annotated[str, typer.Option(
        help="RabbitMQ password.", rich_help_panel="Customization and Utils"
    )],
    file_path: Annotated[
        str,
        typer.Option(
            help="Path to the '.csv' file.",
            rich_help_panel="Customization and Utils",
        ),
    ] = ".",
) -> None:
    """Plusblish messages to RabbitMQ broker."""
    reader = Reader(path=file_path)
    bytes_seralizar = serializers.bytes.Serializer()
    
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

    # Start reading the data as a stream
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
