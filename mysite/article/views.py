import json
from typing import Any, Dict, List, Tuple

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from article import repo
from article.repo import ArticleRepo
from domain import article

# Create your views here.


class _Mapper:

    def _article_to_dto(self, art: article.Article) -> Dict[str, Any]:
        return {
            "id": art.id,
            "title": art.title,
            "description": art.description,
            "image": {
                "url": art.image.url,
            },
            "updatedAt": art.updated_at.isoformat(),
        }


class ArticlesView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._use_case = article.UseCase(repo.ArticleRepo())
        self._mapper = _Mapper()

    def post(self, request):
        data = json.loads(request.POST["json"])

        article_id = self._use_case.insert_or_update_article(article.ArticleInput(
            title=data["title"],
            description=data["description"],
            image=request.FILES.get(data.get("imageRef")),
        ))

        bann = self._use_case.get_article(article_id)

        return Response(status=status.HTTP_201_CREATED, data=self._mapper._article_to_dto(bann))

    def get(self, request):
        articles, cursor = self._get_by_cursor(request, cursor=request.query_params.get(
            "cursor"), limit=request.query_params.get("limit"))
        return Response(status=status.HTTP_200_OK, data={
            "cursor": cursor,
            "items": [self._mapper._article_to_dto(article) for article in articles],
        })

    def _get_by_cursor(self,
                       request,
                       cursor,
                       limit) -> Tuple[List[article.Article], article.Cursor]:
        articles, cursor = self._use_case.get_articles(article.QueryOption(
            cursor=cursor,
            limit=limit,
        ))
        return articles, cursor


class ArticleView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._use_case = article.UseCase(repo.ArticleRepo())
        self._mapper = _Mapper()

    def get(self, request, id):
        try:
            bann = self._use_case.get_article(id=int(id))
            return Response(status=status.HTTP_200_OK, data=self._mapper._article_to_dto(bann))
        except article.ArticleNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND, data=f"article({id}) is not found")

    def patch(self, request, id):
        data = json.loads(request.POST["json"])
        try:
            _ = self._use_case.insert_or_update_article(article.ArticleInput(
                id=int(id),
                title=data["title"],
                description=data["description"],
                image=request.FILES.get(data.get("imageRef")) if data.get("imageRef") else None,
            ))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except article.ArticleNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND, data=f"article({id}) is not found")
