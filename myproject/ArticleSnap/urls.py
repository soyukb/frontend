from django.urls import path, include
from . import views
from .views import (
    ArticleAPIView, PostAPIView, MediaAPIView, CategoryAPIView,
    ArticleCategoryAPIView, PostMediaAPIView, CommentAPIView, ArticleMediaAPIView
)

urlpatterns = [
    # path('item/', views.ItemView.as_view(),name='item'),
    path('articles/', ArticleAPIView.as_view()),
    path('articles/<int:pk>/', ArticleAPIView.as_view()),
    path('posts/', PostAPIView.as_view()),
    path('posts/<int:pk>/', PostAPIView.as_view()),
    path('media/', MediaAPIView.as_view()),
    path('media/<int:pk>/', MediaAPIView.as_view()),
    path('categories/', CategoryAPIView.as_view()),
    path('categories/<int:pk>/', CategoryAPIView.as_view()),
    # path('comments/', CommentAPIView.as_view()),
    # path('comments/<int:pk>/', CommentAPIView.as_view()),
    
    # path('article-categories/', ArticleCategoryAPIView.as_view()),
    # path('article-categories/<int:pk>/', ArticleCategoryAPIView.as_view()),
    # path('post-media/', PostMediaAPIView.as_view()),
    # path('post-media/<int:pk>/', PostMediaAPIView.as_view()), 
    # path('article-media/', ArticleMediaAPIView.as_view()),
    # path('article-media/<int:pk>/', ArticleMediaAPIView.as_view()),
]
