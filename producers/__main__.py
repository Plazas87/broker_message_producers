"""Producers package entrypoint."""
from typing_extensions import Annotated
import typer
from .infrastructure.data_readers.csv import Reader
from .infrastructure.serializers.bytes import Serializer
from .infrastructure.clients.kafka import Producer

app = typer.Typer(rich_markup_mode="rich")

@app.command()
def kafka(
    host: Annotated[str, typer.Option(
        help="Bootstrap server host.", rich_help_panel="Customization and Utils"
    )],
    port: Annotated[int, typer.Option(
        help="Bootstrap server port.", rich_help_panel="Customization and Utils"
    )],
    topic: Annotated[str, typer.Option(
        help="Topic to publish message to.", rich_help_panel="Customization and Utils"
    )],
    partition: Annotated[int, typer.Option(
        help="Topic's partition.", rich_help_panel="Customization and Utils"
    )],
    file_path: Annotated[str, typer.Option(
        help="Path to the '.csv' file.",
        rich_help_panel="Customization and Utils",
    )] = "."
) -> None:
    """Publish messages to a kafka broker."""
    producer = Producer(
        data_source=Reader(path=file_path),
        serializer=Serializer(),
        bootstrap_server_host=host,
        bootstrap_server_port=port,
        topic=topic,
        partition=partition
    )

    producer.publish()


@app.command()
def rabbit_mq():
    """Plusblish messages to RabbitMQ."""
    # TODO: implement the code to plublish messages to RabbitMQ


if __name__ == "__main__":
    app()