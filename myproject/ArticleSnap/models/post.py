from django.db import models
from .media import Media 
from django.utils.timezone import now

class Post(models.Model):
    
    # 投稿ID（自動生成）
    post_id = models.AutoField(primary_key=True)
    
    # 外部キー: Article
    article = models.ForeignKey('Article', on_delete=models.CASCADE, verbose_name="記事", related_name='posts')
    
    # 投稿内容
    content = models.TextField(verbose_name="投稿内容")
    
    # 親投稿ID（自己参照型外部キー）
    parent_post = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, verbose_name="親投稿", related_name="replies"
    )
    
    # いいね数
    likes = models.IntegerField(default=0, verbose_name="いいね数")
    
    # 作成日時
    created_at = models.DateTimeField(default=now, verbose_name="作成日時")  # 日時フィールド
    
    # MediaへのMany-to-Manyフィールド
    media = models.ManyToManyField(Media, related_name="post", verbose_name="関連メディア")
    
    # Thing ID
    thingid = models.CharField(null=True, blank=True,max_length=50, verbose_name="Thing ID", default="")
    
    # 深さ（Depth）
    depth = models.IntegerField(verbose_name="深さ", default=0)

    # 親ID（Parent ID）
    parentid = models.CharField(null=True, blank=True,max_length=50, verbose_name="親ID", default="")
    
    class Meta:
        db_table = "posts"
        # verbose_name = "投稿"
        # verbose_name_plural = "投稿"

    def __str__(self):
        return f"Post in Article {self.article_id}: {self.content[:50]}"
