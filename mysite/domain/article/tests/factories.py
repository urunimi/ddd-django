
import factory
from django.utils import timezone

from domain.article import entities


class ImageFactory(factory.Factory):
    class Meta:
        model = entities.Image

    url = "https://picsum.photos/200"


class ArticleFactory(factory.Factory):
    class Meta:
        model = entities.Article

    id = factory.Sequence(lambda n: n + 1)
    title = factory.Sequence(lambda n: f'article title - {n+1}')
    description = factory.Sequence(lambda n: f'article description - {n+1}')

    image = factory.SubFactory(ImageFactory)
    updated_at = timezone.now()
