from django.db import models

class Article(models.Model):
    # 主キー: 自動的にIDを設定
    article_id = models.AutoField(primary_key=True)
    
    # タイトル: 必須フィールド、長文対応
    title = models.TextField(verbose_name="タイトル")
    
    # 公開予定日時: 任意フィールド
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="公開予定日時")
    
    # 公開ステータス: デフォルトで未公開
    is_published = models.BooleanField(default=False, verbose_name="公開済み")
    
    # 引用元URL: 任意フィールド
    source_url = models.URLField(max_length=500, null=True, blank=True, verbose_name="引用元URL")
    
    # 作成日時: 自動設定
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    
    # 更新日時: 自動更新
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    
    # コメント数: キャッシュ用、デフォルト値0
    comment_count = models.IntegerField(default=0, verbose_name="コメント数")

    class Meta:
        db_table = "articles"  # テーブル名を明示的に指定
        verbose_name = "記事"
        verbose_name_plural = "記事"

    def __str__(self):
        return f"{self.title[:50]}..."  # 管理画面で表示する文字列（50文字に省略）