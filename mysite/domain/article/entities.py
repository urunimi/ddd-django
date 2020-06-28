from dataclasses import dataclass
from datetime import datetime


@dataclass
class Image:
    url: str


@dataclass
class Article:
    id: int
    title: str
    description: str
    image: Image

    updated_at: datetime
