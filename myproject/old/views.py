from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from .models import Article, Post, Media, Category, ArticleCategory, PostMedia, Comment, ArticleMedia
from .serializers import (
    ArticleSerializer, PostSerializer, MediaSerializer,
    CategorySerializer, ArticleCategorySerializer,
    PostMediaSerializer, CommentSerializer, ArticleMediaSerializer
)

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
        serializer = self.serializer_class(instance, data=request.data)
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

class ArticleCategoryAPIView(BaseAPIView):
    model = ArticleCategory
    serializer_class = ArticleCategorySerializer

class PostMediaAPIView(BaseAPIView):
    model = PostMedia
    serializer_class = PostMediaSerializer

class CommentAPIView(BaseAPIView):
    model = Comment
    serializer_class = CommentSerializer

class ArticleMediaAPIView(BaseAPIView):
    model = ArticleMedia
    serializer_class = ArticleMediaSerializer

# Create your views here.
class ItemView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self,request):
        return Response({'method':'get'})