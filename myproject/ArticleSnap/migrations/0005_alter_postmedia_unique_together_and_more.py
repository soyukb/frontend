# Generated by Django 5.1.4 on 2025-01-01 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ArticleSnap', '0004_alter_article_options_article_media_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='postmedia',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='postmedia',
            name='media',
        ),
        migrations.RemoveField(
            model_name='postmedia',
            name='post',
        ),
        migrations.AlterModelOptions(
            name='post',
            options={},
        ),
        migrations.AddField(
            model_name='post',
            name='media',
            field=models.ManyToManyField(related_name='post', to='ArticleSnap.media', verbose_name='関連メディア'),
        ),
        migrations.DeleteModel(
            name='ArticleCategory',
        ),
        migrations.DeleteModel(
            name='PostMedia',
        ),
    ]