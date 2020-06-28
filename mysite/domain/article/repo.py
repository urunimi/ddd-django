from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    List,
    Tuple,
)

from domain.article.value_objects import ArticleInput, ArticleId
from domain.article.entities import Article


class Repo(ABC):

    @abstractmethod
    def insert_or_update_article(self, art_input: ArticleInput) -> ArticleId:
        pass

    @abstractmethod
    def get_article(self, art_id: ArticleId) -> Article:
        pass

    @abstractmethod
    def get_articles(self, last_id: ArticleId, limit: int) -> Tuple[List[Article], bool]:
        '''
        Return articles of given last_id and limit.
        If returning finished flag is True, there is nothing left for the future query.

        :param last_id: last queried article's id
        :param limit: maximum length of returning articles

        :return: tuple of articles and a finished flag
        :rtype: Tuple[List[Article], bool]
        '''
        pass
