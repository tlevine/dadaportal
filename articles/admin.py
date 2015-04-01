from django.contrib import admin

from .models import ArticleCache, ArticleTag

admin.site.register(ArticleCache)
admin.site.register(ArticleTag)
