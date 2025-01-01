from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from .models import Article, Post, Media, Category, Comment
from .serializers import (
    ArticleSerializer, PostSerializer, MediaSerializer,
    CategorySerializer, CommentSerializer, UrlSerializer
)
from .logic.search import extract_data_from_html

class BaseAPIView(APIView):
    model = None
    serializer_class = None

    def get(self, request, pk=None):
        if pk:
            instance = self.model.objects.get(pk=pk)
            serializer = self.serializer_class(instance)
        else:
            instances = self.model.objects.all()
            serializer = self.serializer_class(instances, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        instance = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = self.model.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ArticleAPIView(BaseAPIView):
    model = Article
    serializer_class = ArticleSerializer

class PostAPIView(BaseAPIView):
    model = Post
    serializer_class = PostSerializer

class MediaAPIView(BaseAPIView):
    model = Media
    serializer_class = MediaSerializer

class CategoryAPIView(BaseAPIView):
    model = Category
    serializer_class = CategorySerializer

class CommentAPIView(BaseAPIView):
    model = Comment
    serializer_class = CommentSerializer

class RedditAPIView(APIView):
    serializer_class = UrlSerializer
    def post(self, request, *args, **kwargs):
        # ここでリクエストのURLを取得
        input_url = request.data.get('url')
        
        if not input_url:
            return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        response_data = extract_data_from_html(input_url)
        
        # 以下はサンプルデータ（実際にはWebスクレイピングやAPI呼び出しでデータ取得）
        # response_data = {
        #     "title": "Sample Article Title",
        #     "source_url": input_url,
        #     "media": [
        #         {
        #             "media_type": "image",
        #             "media_url": "https://example.com/image1.jpg"
        #         },
        #         {
        #             "media_type": "video",
        #             "media_url": "https://example.com/video1.mp4"
        #         }
        #     ],
        #     "posts": [
        #         {
        #             "content": "This is a sample post content.",
        #             "media": [
        #                 {
        #                     "media_type": "image",
        #                     "media_url": "https://example.com/image1.jpg"
        #                 },
        #                 {
        #                     "media_type": "video",
        #                     "media_url": "https://example.com/video1.mp4"
        #                 }
        #             ]
        #         },
        #         {
        #             "content": "This is another post content.",
        #             "media": [
        #                 {
        #                     "media_type": "image",
        #                     "media_url": "https://example.com/image1.jpg"
        #                 },
        #                 {
        #                     "media_type": "video",
        #                     "media_url": "https://example.com/video1.mp4"
        #                 }
        #             ]
        #         }
        #     ]
        # }
        
        serializer = ArticleSerializer(data=response_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)