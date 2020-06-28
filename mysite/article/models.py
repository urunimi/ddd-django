from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=63, null=True)
    description = models.CharField(max_length=63, null=True)

    image = models.FileField(upload_to='build/article-image')

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'article'
