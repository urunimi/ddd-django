from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TransactionTestCase

from domain.article.entities import Article
from domain.article.errors import ArticleNotFoundError
from domain.article.tests.factories import ArticleFactory
from domain.article.value_objects import ArticleInput
from article.models import Article as DbArticle
from article.repo import (
    ArticleRepo,
    _Mapper,
)
from article.tests.factories import DbArticleFactory


class TestArticleRepo(TransactionTestCase):

    def setUp(self):
        super().setUp()
        self._repo = ArticleRepo()
        self._mapper = _Mapper()

    def test_insert_article(self):
        article = ArticleFactory.create()

        article_id = self._repo.insert_or_update_article(ArticleInput(
            title=article.title,
            description=article.description,
            image=SimpleUploadedFile("article-image", b"content", content_type="image/png"),
        ))

        db_article = DbArticle.objects.get(pk=article_id)
        self.assertEqual(article_id, db_article.id)
        self._assert_equal_article(article, db_article)

    def test_update_article(self):
        prev_db_article = DbArticleFactory.create()
        article = ArticleFactory.create()

        article_id = self._repo.insert_or_update_article(ArticleInput(
            id=prev_db_article.id,
            title=article.title,
            description=article.description,
            image=SimpleUploadedFile("article-image", b"content", content_type="image/png"),
        ))

        db_article = DbArticle.objects.get(pk=article_id)
        self.assertEqual(article_id, db_article.id)
        self._assert_equal_article(article, db_article)

    def test_get_article(self):
        db_article = DbArticleFactory.create()

        article = self._repo.get_article(db_article.id)

        self._assert_equal_article(article, db_article)

    def test_get_article_not_exists(self):
        db_article = DbArticleFactory.create()

        with self.assertRaises(ArticleNotFoundError):
            _ = self._repo.get_article(db_article.id + 1)

    def test_get_articles_by_order(self):
        limit = 10
        count = limit * 2
        db_articles = DbArticleFactory.create_batch(count)

        articles, finished = self._repo.get_articles(
            last_id=0,
            limit=limit)

        db_ids = [db_article.id for db_article in db_articles]

        self.assertEqual(limit, len(articles))
        self.assertEqual(finished, False)
        for article in articles:
            self.assertEqual(article.id in db_ids, True)

    def _assert_equal_article(self, article: Article, db_article: DbArticle):
        self.assertEqual(db_article.title, article.title)
        self.assertEqual(db_article.description, article.description)
