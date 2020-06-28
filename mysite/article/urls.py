from django.urls import path

from article.views import ArticlesView, ArticleView

urlpatterns = [
    path('articles', ArticlesView.as_view(), name='articles'),
    path('articles/<str:id>', ArticleView.as_view(), name='article'),
]
