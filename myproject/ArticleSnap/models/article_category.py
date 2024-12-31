from django.db import models

class ArticleCategory(models.Model):
    # 外部キー: Category
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name="カテゴリー")
    
    # 外部キー: Article
    article = models.ForeignKey('Article', on_delete=models.CASCADE, verbose_name="記事")
    
    class Meta:
        db_table = "article_categories"  # テーブル名
        verbose_name = "記事カテゴリー関連"
        verbose_name_plural = "記事カテゴリー関連"
        unique_together = ('category', 'article')  # 複合ユニーク制約

    def __str__(self):
        return f"{self.article.title} - {self.category.category_name}"
