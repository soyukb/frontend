# Generated by Django 5.1.4 on 2025-01-02 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArticleSnap', '0010_article_title_translated'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content_translated',
            field=models.TextField(blank=True, null=True, verbose_name='翻訳された投稿内容'),
        ),
    ]
