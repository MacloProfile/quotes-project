from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path
from django import forms
from app.models.quote import Quote


class BulkQuotesForm(forms.Form):
    quotes_text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 15, "cols": 100}),
        label="Цитаты (по одной в строке, формат: цитата — источник)"
    )


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('quote', 'source', 'weight', 'views', 'likes', 'dislikes', 'status', 'moderation_comment')
    list_filter = ('status', 'weight')
    search_fields = ('quote', 'source')
    actions = ['approve_quotes', 'reject_quotes']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-add/', self.admin_site.admin_view(self.bulk_add_view), name='bulk-add-quotes'),
        ]
        return custom_urls + urls

    def bulk_add_view(self, request):
        if request.method == "POST":
            form = BulkQuotesForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data['quotes_text']
                added = 0
                skipped = 0

                for line in text.splitlines():
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split(' | ')
                    if len(parts) == 2:
                        quote_text, source = parts
                    else:
                        quote_text = line
                        source = "Неизвестно"

                    if not Quote.objects.filter(quote=quote_text).exists():
                        Quote.objects.create(
                            quote=quote_text,
                            source=source,
                            status=True,
                            moderation_comment="✅ Добавлено администратором"
                        )
                        added += 1
                    else:
                        skipped += 1

                messages.success(
                    request,
                    f"✅ Добавлено: {added}, пропущено (дубликаты): {skipped}."
                )
                return redirect("..")
        else:
            form = BulkQuotesForm()

        return render(request, "admin/bulk_add_quotes.html", {"form": form})

    def approve_quotes(self, request, queryset):
        queryset.update(status=True, moderation_comment='✅ Одобрено модератором')
    approve_quotes.short_description = "Одобрить выбранные цитаты"

    def reject_quotes(self, request, queryset):
        queryset.update(status=False, moderation_comment='❌ Отклонено модератором')
    reject_quotes.short_description = "Отклонить выбранные цитаты"
