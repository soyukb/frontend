from django.db import models

class Media(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('gif', 'GIF'),
    ]
    
    media_type = models.CharField(
        max_length=50,
        choices=MEDIA_TYPE_CHOICES,
        default='image'
    )
    media_url = models.URLField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.media_type}: {self.media_url}"
