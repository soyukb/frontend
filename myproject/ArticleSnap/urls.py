from django.urls import path, include
from . import views
from .views import (
    ArticleAPIView, PostAPIView, MediaAPIView, CategoryAPIView,
    CommentAPIView, RedditAPIView
)

urlpatterns = [
    path('articles/', ArticleAPIView.as_view()),
    path('articles/<int:pk>/', ArticleAPIView.as_view()),
    # path('posts/', PostAPIView.as_view()),
    # path('posts/<int:pk>/', PostAPIView.as_view()),
    # path('media/', MediaAPIView.as_view()),
    # path('media/<int:pk>/', MediaAPIView.as_view()),
    # path('categories/', CategoryAPIView.as_view()),
    # path('categories/<int:pk>/', CategoryAPIView.as_view()),
    path('comments/', CommentAPIView.as_view()),
    # path('comments/<int:pk>/', CommentAPIView.as_view()),
    path('reddit/', RedditAPIView.as_view()),

]
