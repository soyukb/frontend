from django.db import models

class PostMedia(models.Model):
    post = models.ForeignKey(
        'Post', 
        on_delete=models.CASCADE, 
        related_name='post_medias'
    )
    media = models.ForeignKey(
        'Media', 
        on_delete=models.CASCADE, 
        related_name='media_posts'
    )
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'media')

    def __str__(self):
        return f"Post: {self.post.id}, Media: {self.media.id}, Primary: {self.is_primary}"
