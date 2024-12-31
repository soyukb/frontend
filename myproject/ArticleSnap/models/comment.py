from django.db import models

class Comment(models.Model):
    # コメントID（自動生成）
    comment_id = models.BigAutoField(primary_key=True)
    
    # 外部キー: Article
    article = models.ForeignKey('Article', on_delete=models.CASCADE, verbose_name="記事")
    
    # コメント内容
    content = models.TextField(verbose_name="コメント内容")
    
    # 投稿者
    author = models.CharField(max_length=100, null=True, blank=True, verbose_name="投稿者")
    
    # 作成日時
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    
    # 親コメントID（自己参照型外部キー）
    parent_comment = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, verbose_name="親コメント", related_name="replies"
    )
    
    # いいねと低評価
    likes = models.IntegerField(default=0, verbose_name="いいね数")
    dislikes = models.IntegerField(default=0, verbose_name="低評価数")

    class Meta:
        db_table = "comments"
        verbose_name = "コメント"
        verbose_name_plural = "コメント"

    def __str__(self):
        return f"{self.content[:50]}..."  # 内容を50文字に省略
