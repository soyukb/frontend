from django.db import models

class ArticleMedia(models.Model):
    article = models.ForeignKey(
        'Article',
        on_delete=models.CASCADE,
        related_name='article_medias'
    )
    media = models.ForeignKey(
        'Media',
        on_delete=models.CASCADE,
        related_name='media_articles'
    )
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('article', 'media')

    def __str__(self):
        return f"Article: {self.article.article_id}, Media: {self.media.id}, Primary: {self.is_primary}"
