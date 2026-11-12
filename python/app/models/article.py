from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Article:
    id: str
    title: str
    link: str
    author: str
    published: Optional[datetime]
    source: str
    text: str
