"""CSV file data reader module."""
import pathlib
import time
from typing import Dict, Generator
from . import IReader
import pandas as pd


class Reader(IReader[Dict[str, int]]):
    """Reader class."""

    def __init__(self, path: str) -> None:
        """Class constructor."""
        self._path = pathlib.Path(path)

    def read(self) -> Generator[Dict[str, int], None, None]:
        """Read data from a .csv file and return it as generator.

        Yields:
            Generator[Dict[str, int], None, None]: data generator.
        """
        # Suppose the file that we are going to read could be huge and load it
        # completely in memory could crash your running process.
        # To avoid this, we are going to fetch chunks of data a fixed size.
        for chunk in pd.read_csv(self._path, chunksize=10):
            for measurement in chunk.itertuples(name="Measurement"):
                time.sleep(1)  # simulates a sample rate of 1 second for a sensor
                yield {"temperature": measurement.temperature}
