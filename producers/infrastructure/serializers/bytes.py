"""Json serializer module."""

import json
from typing import Any, Dict
from ...application.ports import ISerializer


class Serializer(ISerializer[Dict[str, Any], bytes]):
    """Serializer class."""

    def serialize(self, data: Dict[str, Any]) -> bytes:
        """Serialize a json object to bytes."""
        return json.dumps(data).encode('utf-8')