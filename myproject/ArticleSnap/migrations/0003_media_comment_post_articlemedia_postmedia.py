# Generated by Django 5.1.4 on 2024-12-31 02:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArticleSnap', '0002_article_category_articlecategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video'), ('audio', 'Audio'), ('gif', 'GIF')], default='image', max_length=50)),
                ('media_url', models.URLField(max_length=2048)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(verbose_name='コメント内容')),
                ('author', models.CharField(blank=True, max_length=100, null=True, verbose_name='投稿者')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('likes', models.IntegerField(default=0, verbose_name='いいね数')),
                ('dislikes', models.IntegerField(default=0, verbose_name='低評価数')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ArticleSnap.article', verbose_name='記事')),
                ('parent_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='ArticleSnap.comment', verbose_name='親コメント')),
            ],
            options={
                'verbose_name': 'コメント',
                'verbose_name_plural': 'コメント',
                'db_table': 'comments',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(verbose_name='投稿内容')),
                ('likes', models.IntegerField(default=0, verbose_name='いいね数')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ArticleSnap.article', verbose_name='記事')),
                ('parent_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='ArticleSnap.post', verbose_name='親投稿')),
            ],
            options={
                'verbose_name': '投稿',
                'verbose_name_plural': '投稿',
                'db_table': 'posts',
            },
        ),
        migrations.CreateModel(
            name='ArticleMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_primary', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_medias', to='ArticleSnap.article')),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media_articles', to='ArticleSnap.media')),
            ],
            options={
                'unique_together': {('article', 'media')},
            },
        ),
        migrations.CreateModel(
            name='PostMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_primary', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media_posts', to='ArticleSnap.media')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_medias', to='ArticleSnap.post')),
            ],
            options={
                'unique_together': {('post', 'media')},
            },
        ),
    ]