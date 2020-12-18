from dataclasses import dataclass
from typing import Dict, Any

from ..helpers import default


@dataclass
class Record:
    table: str = None
    from_index: str = None
    attributes: Dict[str, Any] = default(dict)
