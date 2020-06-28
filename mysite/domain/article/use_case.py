import base64
from typing import List, Tuple

from domain.article.entities import Article
from domain.article.repo import Repo
from domain.article.value_objects import (ArticleId, ArticleInput, Cursor,
                                          QueryOption)


class UseCase:
    def __init__(self, repo: Repo):
        super().__init__()
        self._repo = repo

    def insert_or_update_article(self, article: ArticleInput) -> ArticleId:
        '''
        Insert or update article into repository.
        If input's opened_at is None, now() will be set.

        :param article: article input object

        :raises ArticleNotFoundError: when article of given id is not found,
                    ArticleNotFoundError is raised.

        :return: the id of article
        :rtype: ArticleId
        '''
        return self._repo.insert_or_update_article(article)

    def get_article(self, id: ArticleId) -> Article:
        '''
        Get article of given id.

        :param id: id of article

        :raises ArticleNotFoundError: when article of given id is not found,
                    ArticleNotFoundError is raised.

        :return: article of given id
        :rtype: Optional[Article]
        '''
        return self._repo.get_article(id)

    def get_articles(self, option: QueryOption) -> Tuple[List[Article], Cursor]:
        '''
        Get articles in the context of given cursor based query option.
        If next cursor is None, there is nothing left for next query.

        :param option: query option

        :return: tuple of articles and next cursor
        :rtype: Tuple[List[Article], str]
        '''
        last_id = -1
        if option.cursor:
            last_id = self._parse_cursor(option.cursor)

        articles, finished = self._repo.get_articles(last_id, option.limit)

        cursor = None
        if articles and not finished:
            cursor = self._build_cursor(last_id=articles[-1].id)

        return articles, cursor

    def _parse_cursor(self, cursor: Cursor) -> int:
        return int(base64.b64decode(cursor).decode("UTF-8"))

    def _build_cursor(self, last_id: ArticleId) -> Cursor:
        return base64.b64encode(str(last_id).encode("UTF-8")).decode("UTF-8")
