# serializers.py
from rest_framework import serializers
from ..models import Article, Post, Media, Category, ArticleCategory, PostMedia, Comment, ArticleMedia
import logging

logger = logging.getLogger(__name__)

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['media_type', 'media_url']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = '__all__'

class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ArticleMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleMedia
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer): 
    media = MediaSerializer(many=True,read_only=True,source='post_medias.media')
    class Meta:
        model = Post
        fields = ['content', 'media']

    def create(self, validated_data):
        # ネストされた 'media' データを取り出す
        media_data = validated_data.pop('media', [])
        
        # Post モデルのインスタンスを作成
        post = Post.objects.create(**validated_data)
        
        # 'media' データを処理
        for media in media_data:
            # Media モデルのインスタンスを取得または新規作成
            media_instance, _ = Media.objects.get_or_create(**media)
            
            # PostMedia を作成し、Post と Media を関連付ける
            PostMedia.objects.create(post=post, media=media_instance)
        
        # 作成した Post インスタンスを返す
        return post


class ArticleSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True,read_only=True,source='article_medias.media')  # ネストされたメディアデータ
    posts = PostSerializer(many=True,read_only=True)  # ネストされた投稿データ
    class Meta:
        model = Article
        fields = ['title', 'media', 'posts']

    def create(self, validated_data):
        logger.debug(f"Validated data: {validated_data}")  # 検証済みデータをログに出力
        # ネストされた 'media' データを取り出す
        media_data = validated_data.pop('media', [])
        
        # ネストされた 'posts' データを取り出す
        posts_data = validated_data.pop('posts', [])
        
        # Article モデルのインスタンスを作成
        article = Article.objects.create(**validated_data)

        
        # 'media' データを処理
        for media in media_data:
            # Media モデルのインスタンスを取得または新規作成
            media_instance, _ = Media.objects.get_or_create(**media)
            print(media_instance)
            # PostMedia を作成し、Post と Media を関連付ける
            ArticleMedia.objects.create(article=article, media=media_instance)
               
        # 'posts' データを処理
        for post_data in posts_data:
            # Post の 'media' を取り出す
            post_media_data = post_data.pop('media', [])
            
            # PostSerializer を利用して Post データを検証・保存
            post_serializer = PostSerializer(data=post_data)
            if post_serializer.is_valid():
                # Post の 'article' フィールドを設定し保存
                post_instance = post_serializer.save(article=article)
                print(post_instance)
                
                # 'media' データを処理して Post と Media を関連付ける
                for post_media in post_media_data:
                    # Media モデルのインスタンスを取得または新規作成
                    media_instance, _ = Media.objects.get_or_create(**post_media)
                    
                    # PostMedia を作成し、Post と Media を関連付ける
                    PostMedia.objects.create(post=post_instance, media=media_instance)
            
        # 作成した Article インスタンスを返す
        return article