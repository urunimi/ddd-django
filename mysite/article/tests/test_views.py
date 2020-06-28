from unittest.mock import ANY, patch

from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import resolve_url
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from domain.article.tests.factories import ArticleFactory
from domain.article.value_objects import ArticleInput, QueryOption


@patch("article.repo.ArticleRepo")
class TestArticleView(APITestCase):

    def setUp(self):
        super().setUp()
        self.user = AnonymousUser()
        self.client.force_authenticate(self.user)

    def test_get(self, _):
        bann = ArticleFactory.create()
        with patch("services.article.rest.article.UseCase") as uc_class:
            use_case = uc_class.return_value
            use_case.get_article.return_value = bann

            res = self.client.get(resolve_url("article", id=bann.id))

            self.assertEqual(res.status_code, status.HTTP_200_OK, res.data)
            res_article = res.data["data"]
            self.assertEqual(res_article["id"], bann.id)
            self.assertEqual(res_article["title"], bann.title)
            self.assertEqual(res_article["description"], bann.description)
            self.assertEqual(res_article["image"]["url"], bann.image.url)

            use_case.get_article.assert_called_once_with(id=bann.id)

    def test_patch(self, _):
        article = ArticleFactory.create()
        data = {
            "title": article.title,
            "description": article.description,
            "imageRef": "image",
        }
        kwargs = {
            "image": SimpleUploadedFile("image.png", b"content", "image/png"),
        }
        with patch("article.rest.article.UseCase") as uc_class:
            use_case = uc_class.return_value
            use_case.insert_or_update_article.return_value = article.id

            kwargs["json"] = data

            res = self.client.patch(resolve_url("article", id=article.id), data=kwargs, format='multipart')

            self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT, res.data)
            use_case.insert_or_update_article.assert_called_once_with(ArticleInput(
                id=article.id,
                title=data["title"],
                description=data["description"],
                image=ANY,
            ))


@patch("services.article.repo.ArticleRepo")
class TestArticlesView(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = AnonymousUser()
        self.client.force_authenticate(self.user)
        self.url = reverse('articles')

    def test_post(self, _):
        article = ArticleFactory.create()
        data = {
            "title": article.title,
            "description": article.description,
            "imageRef": "image",
        }
        kwargs = {
            "image": SimpleUploadedFile("image.png", b"content", "image/png"),
        }
        with patch("services.article.rest.article.UseCase") as uc_class:
            use_case = uc_class.return_value
            use_case.insert_or_update_article.return_value = article.id
            use_case.get_article.return_value = article
            kwargs["json"] = data

            res = self.client.patch(resolve_url("articles", id=article.id), data=kwargs, format='multipart')

            self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.data)
            use_case.insert_or_update_article.assert_called_once_with(ArticleInput(
                title=data["title"],
                description=data["description"],
                image=ANY,
            ))

    def test_get_by_cursor(self, _):
        articles = ArticleFactory.create_batch(4)
        cursor, next_cursor = "cursor", "nextCursor"

        with patch("services.article.rest.article.UseCase") as uc_class:
            use_case = uc_class.return_value
            use_case.get_articles_by_cursor.return_value = (articles, next_cursor)

            res = self.client.get(self.url, data={"cursor": cursor})

            self.assertEqual(res.status_code, status.HTTP_200_OK, res.data)
            use_case.get_articles_by_cursor.assert_called_once_with(QueryOption(
                cursor=cursor,
                limit=ANY,
            ))
            self._assert_equal_articles(articles=articles, data=res.data["items"])
            self.assertEqual(next_cursor, res.data["cursor"])

    def _assert_equal_articles(self, articles, data):
        for i in range(len(articles)):
            self.assertEqual(articles[i].id, data[i]["id"])
            self.assertEqual(articles[i].title, data[i]["title"])
            self.assertEqual(articles[i].description, data[i]["description"])
            self.assertEqual(articles[i].image.url, data[i]["image"]["url"])
