import datetime
import random
from unittest import TestCase
from unittest.mock import MagicMock

from domain import article
from domain.article.tests.factories import ArticleFactory
from django.utils import timezone


class TestArticleUseCase(TestCase):

    def setUp(self):
        super().setUp()
        self.repo = MagicMock()
        self.use_case = article.UseCase(self.repo)

    def test_insert_or_update_article(self):
        # Given
        article_id = random.randint(1, 100)
        self.repo.insert_or_update_article.return_value = article_id
        article_input = article.ArticleInput(
            title="article title",
            description="article description",
            image=None,
        )

        # When
        res = self.use_case.insert_or_update_article(article_input)

        # Then
        self.assertEqual(res, article_id)
        self.repo.insert_or_update_article.assert_called_once_with(article_input)

    def test_get_article(self):
        art = ArticleFactory.create()
        self.repo.get_article.return_value = art

        res = self.use_case.get_article(art.id)

        self.assertEqual(res, art)
        self.repo.get_article.assert_called_once_with(art.id)

    def test_get_articles(self):
        size = random.randint(5, 20)
        cursor_option = article.QueryOption(
            limit=10,
            cursor="MTA=",  # 10
        )
        cursor = "MjA="  # 20
        articles = ArticleFactory.create_batch(size)
        articles[-1].id = 20
        self.repo.get_articles_by_order.return_value = (articles, False)

        res_articles, res_cursor = self.use_case.get_articles_by_cursor(cursor_option)

        self.assertEqual(articles, res_articles)
        self.assertEqual(cursor, res_cursor)
        self.repo.get_articles_by_order.assert_called_once_with(cursor_option.statuses, 10, cursor_option.limit)
