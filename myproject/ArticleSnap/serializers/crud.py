# serializers.py
from rest_framework import serializers
from ..models import Article, Post, Media, Category, Comment
from django.db import transaction
from django.db.models import F

class UrlSerializer(serializers.Serializer):
    url = serializers.URLField()

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['media_type', 'media_url']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        
    def create(self, validated_data):
        with transaction.atomic():
            # コメントを作成
            comment = super().create(validated_data)            
            # 関連するArticleのcomment_countを1増やす
            article = comment.article  # CommentモデルにForeignKeyでArticleが関連付いていると仮定
            article.comment_count = F('comment_count') + 1
            article.save(update_fields=['comment_count'])
        
        return comment

class PostSerializer(serializers.ModelSerializer): 
    media = MediaSerializer(many=True, required=False)
    class Meta:
        model = Post
        fields = ['content', 'content_translated','media','thingid','depth','parentid','created_at','likes']
        read_only_fields = []
        
    def create(self, validated_data):
        # ネストされた 'media' データを取り出す
        media_data = validated_data.pop('media', [])
        
        # Post モデルのインスタンスを作成
        post = Post.objects.create(**validated_data)
        
        # 'media' データを処理
        for media in media_data:
            # Media モデルのインスタンスを取得または新規作成
            media_instance, _ = Media.objects.get_or_create(**media)
            post.media.add(media_instance)
        
        # 作成した Post インスタンスを返す
        return post

class ArticleSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True)
    posts = PostSerializer(many=True) 
    category = CategorySerializer(many=True, required=False)     
    class Meta:
        model = Article
        fields = ['article_id','title','title_translated','source_url','category','published_at','comment_count','is_published','media', 'posts']
        read_only_fields = ['article_id',]
        
    def create(self, validated_data):
        with transaction.atomic():
            # ネストされた 'media' データを取り出す
            media_data = validated_data.pop('media', [])
            
            # ネストされた 'posts' データを取り出す
            posts_data = validated_data.pop('posts', [])
            
            # ネストされた 'category' データを取り出す
            category_data = validated_data.pop('category', [])
            
            
            # Article モデルのインスタンスを作成
            article_instance = Article.objects.create(**validated_data)
            
            

            # 'media' データを処理
            for media in media_data:
                # Media モデルのインスタンスを取得または新規作成
                media_instance, _ = Media.objects.get_or_create(**media)
                article_instance.media.add(media_instance)
            
            # 'category' データを処理
            for category in category_data:
                # Media モデルのインスタンスを取得または新規作成
                category_instance, _ = Category.objects.get_or_create(**category)
                article_instance.category.add(category_instance)
                
            # 'posts' データを処理
            for post_data in posts_data:
                # 'article_id' を post_data に追加
                post_data['article_id'] = article_instance.article_id
                # Post の 'media' を取り出す
                post_media_data = post_data.pop('media', [])
                post_instance, _ = Post.objects.get_or_create(**post_data)

                # 'media' データを処理
                for media in post_media_data:
                    # Media モデルのインスタンスを取得または新規作成
                    media_instance, _ = Media.objects.get_or_create(**media)
                    post_instance.media.add(media_instance)
                        
            # 作成した Article インスタンスを返す
            return article_instance
        
    def update(self, instance, validated_data):
        with transaction.atomic():
            # ネストされた 'media' データを取り出す
            media_data = validated_data.pop('media', [])
            
            # ネストされた 'posts' データを取り出す
            posts_data = validated_data.pop('posts', [])
            
            # ネストされた 'category' データを取り出す
            category_data = validated_data.pop('category', [])
            
            # Article モデルのフィールドを更新
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            # 'media' データを処理
            if media_data:
                # 現在の関連付けをクリア
                instance.media.clear()
                for media in media_data:
                    # Media モデルのインスタンスを取得または新規作成
                    media_instance, _ = Media.objects.get_or_create(**media)
                    instance.media.add(media_instance)
            
            # 'posts' データを処理
            if posts_data:
                # 現在の関連付けを削除（再構築するため）
                instance.posts.all().delete()
                for post_data in posts_data:
                    # 'article_id' を post_data に追加
                    post_data['article_id'] = instance.article_id
                    # Post の 'media' を取り出す
                    post_media_data = post_data.pop('media', [])
                    post_instance = Post.objects.create(**post_data)

                    # 'media' データを処理
                    for media in post_media_data:
                        # Media モデルのインスタンスを取得または新規作成
                        media_instance, _ = Media.objects.get_or_create(**media)
                        post_instance.media.add(media_instance)
            
            # 'media' データを処理
            if category_data:
                # 現在の関連付けをクリア
                instance.category.clear()
                for category in category_data:
                    # Media モデルのインスタンスを取得または新規作成
                    category_instance, _ = Category.objects.get_or_create(**category)
                    instance.category.add(category_instance)
            
            # 更新した Article インスタンスを返す
            return instance