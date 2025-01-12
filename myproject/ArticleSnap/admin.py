from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Article, Post, Media, Category, Comment
from django.apps import apps

# Postのインライン編集設定
class PostInline(admin.TabularInline):
    model = Post
    extra = 1  # 新規データの入力行を1つ表示

# Commentのインライン編集設定
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # コメント用に2つの入力フィールドを表示

# Articleの管理画面でPost, Media, Commentを同時編集できるように
class ArticleAdmin(admin.ModelAdmin):
    inlines = [PostInline, CommentInline]
    # list_display = ('title', 'category')  # 一覧画面の表示カラム設定
    readonly_fields = ('article_id',)
    list_display = ('article_id','title_translated','title')

# Categoryの通常登録
admin.site.register(Category)
admin.site.register(Media)
# Articleのカスタム登録
admin.site.register(Article, ArticleAdmin)



# # アプリケーション内のすべてのモデルを取得
# app = apps.get_app_config('ArticleSnap')  # 'myapp' はアプリケーション名

# for model_name, model in app.models.items():
#     admin.site.register(model)

