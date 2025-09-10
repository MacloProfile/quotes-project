from django.contrib import admin

from app.models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('quote', 'source', 'weight', 'views', 'likes', 'dislikes')
