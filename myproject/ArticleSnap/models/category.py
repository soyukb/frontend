from django.db import models

class Category(models.Model):
    # 主キー: 自動インクリメント
    category_id = models.AutoField(primary_key=True)
    
    # カテゴリー名: 必須フィールド、一意制約
    category_name = models.CharField(max_length=255, unique=True, verbose_name="カテゴリー名")
    
    class Meta:
        db_table = "categories"  # テーブル名を明示的に指定
        verbose_name = "カテゴリー"
        verbose_name_plural = "カテゴリー"

    def __str__(self):
        return self.category_name  # 管理画面で表示する文字列
