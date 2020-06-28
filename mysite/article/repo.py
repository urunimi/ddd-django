from typing import (
    List,
    Tuple,
)

from domain import article
from domain.article.errors import (
    ArticleNotFoundError,
)
from article import models


class _Mapper():

    def to_article_entity(self, db_article: models.Article) -> article.Article:
        return article.Article(
            id=db_article.id,
            title=db_article.title,
            description=db_article.description,
            image=article.Image(url=db_article.image.url),
            updated_at=db_article.updated_at,
        )


class ArticleRepo(article.Repo):

    def __init__(self):
        super().__init__()
        self._mapper = _Mapper()

    def insert_or_update_article(self, art_input: article.ArticleInput) -> article.ArticleId:
        db_article = None
        if art_input.id:
            try:
                db_article = models.Article.objects.get(id=art_input.id)
            except models.Article.DoesNotExist:
                raise ArticleNotFoundError()
        else:
            db_article = models.Article()

        db_article.title = art_input.title
        db_article.description = art_input.description
        if art_input.image:
            db_article.image = art_input.image
        db_article.save()

        return db_article.id

    def get_article(self, art_id: article.ArticleId) -> article.Article:
        try:
            db_article = models.Article.objects.get(pk=art_id)
            return self._mapper.to_article_entity(db_article=db_article)
        except models.Article.DoesNotExist:
            raise ArticleNotFoundError()

    def get_articles(self,
                     last_id: article.ArticleId,
                     limit: int) -> Tuple[List[article.Article], bool]:
        qs = models.Article.objects

        if last_id:
            last_article = models.Article.objects.get(pk=last_id)
            qs = qs.filter(id_gt=last_article.id)
        else:
            qs = qs.all()

        result = qs[:limit]
        articles = [self._mapper.to_article_entity(m) for m in result]

        return articles, len(result) < limit
