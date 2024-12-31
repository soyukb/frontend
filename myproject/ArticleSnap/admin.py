from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

from django.apps import apps

# アプリケーション内のすべてのモデルを取得
app = apps.get_app_config('ArticleSnap')  # 'myapp' はアプリケーション名

for model_name, model in app.models.items():
    admin.site.register(model)

