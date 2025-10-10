from django.core.exceptions import ValidationError
from django.db import models


class Quote(models.Model):
    quote = models.TextField(unique=True, error_messages={
        'unique': "Такая цитата уже есть в базе."
    })
    source = models.CharField(max_length=255)
    weight = models.PositiveIntegerField(default=1)
    views = models.PositiveIntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    created_at_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        help_text="Статус модерации: True — одобрено, False — отклонено, None — ещё не проверено."
    )
    moderation_comment = models.TextField(
        blank=True,
        null=True,
        help_text="Комментарий модератора или ИИ о причине отказа/одобрения."
    )

    objects = models.Manager()

    def clean(self):
        if Quote.objects.filter(source=self.source).exclude(pk=self.pk).count() >= 99:
            raise ValidationError(f'Для источника "{self.source}" уже есть 99 цитаты.')
        if self.weight < 1 or self.weight > 3:
            raise ValidationError("Вес цитаты должен быть в диапазоне от 1 до 3.")
        if len(self.quote) > 300:
            raise ValidationError("Слишком длинная цитата (максимум 300 символов)")
        if len(self.quote) < 3:
            raise ValidationError("Слишком короткая цитата (минимум 3 символов)")

    def like(self):
        self.likes += 1
        self.save(update_fields=['likes'])

    def dislike(self):
        self.dislikes += 1
        self.save(update_fields=['dislikes'])
