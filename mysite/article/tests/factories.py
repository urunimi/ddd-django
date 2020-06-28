import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from factory import DjangoModelFactory

from article.models import Article


class DbArticleFactory(DjangoModelFactory):

    class Meta:
        model = Article

    title = factory.Sequence(lambda n: f'name-{n}')
    description = factory.Sequence(lambda n: f'name-{n}')
    image = SimpleUploadedFile('filename', b'content')

    updated_at = timezone.now()
    created_at = timezone.now()
