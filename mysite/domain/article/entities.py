from dataclasses import dataclass


@dataclass
class Image:
    url: str


@dataclass
class Article:
    id: int
    title: str
    description: str
    image: Image
