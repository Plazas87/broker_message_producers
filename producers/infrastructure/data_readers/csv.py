"""CSV file data reader module."""
import pathlib
import time
from typing import Any, Dict, Generator

import pandas as pd

from . import IReader


class Reader(IReader[Dict[str, Any]]):
    """Reader class."""

    def __init__(self, path: str) -> None:
        """Class constructor."""
        self._path = pathlib.Path(path)

    def read(self) -> Generator[Dict[str, Any], None, None]:
        """Read data from a .csv file and return it as generator.

        Yields:
            Generator[Dict[str, int], None, None]: data generator.
        """
        # Suppose the file that we are going to read could be huge and load it
        # completely in memory could crash your running process.
        # To avoid this, we are going to fetch fixed size chunks of data.
        for chunk in pd.read_csv(self._path, chunksize=10):
            for measurement in chunk.itertuples(name="Measurement"):
                time.sleep(5)  # simulates a sample rate of 5 second for a sensor
                yield {
                    "temperature": measurement.temperature,
                    "timestamp": measurement.timestamp,
                }
