from dataclasses import dataclass
from typing import (
    Optional,
)

from domain.common.file import (
    File,
)

ArticleId = int
Cursor = str


@dataclass(frozen=True)
class ArticleInput:

    title: str
    description: str

    id: Optional[int] = None
    image: Optional[File] = None


@dataclass(frozen=True)
class QueryOption:
    '''
    :ivar limit: query limit
    :ivar cursor: cursor value or `None`.
    '''
    limit: int
    cursor: Optional[Cursor] = None
