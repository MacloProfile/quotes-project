from django.contrib import admin
from app.models.quote import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('quote', 'source', 'weight', 'views', 'likes', 'dislikes', 'status', 'moderation_comment')
    list_filter = ('status', 'weight')
    search_fields = ('quote', 'source')
    actions = ['approve_quotes', 'reject_quotes']

    def approve_quotes(self, request, queryset):
        queryset.update(status=True, moderation_comment='✅ Одобрено модератором')
    approve_quotes.short_description = "Одобрить выбранные цитаты"

    def reject_quotes(self, request, queryset):
        queryset.update(status=False, moderation_comment='❌ Отклонено модератором')
    reject_quotes.short_description = "Отклонить выбранные цитаты"
