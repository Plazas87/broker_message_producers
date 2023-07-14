"""Json serializer module."""

import json
from typing import Dict
from . import ISerializer


class Serializer(ISerializer[Dict[str, int], bytes]):
    """Serializer class."""

    def serialize(self, data: Dict[str, int]) -> bytes:
        """Serialize a json object to bytes."""
        return json.dumps(data).encode('utf-8')