from django.core.exceptions import ValidationError
from django.db import models


class Quote(models.Model):
    quote = models.TextField(unique=True)
    source = models.CharField(max_length=255)
    weight = models.PositiveIntegerField(default=1)
    views = models.PositiveIntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    created_at_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def clean(self):
        if Quote.objects.filter(source=self.source).exclude(pk=self.pk).count() >= 3:
            raise ValidationError(f'Для источника "{self.source}" уже есть 3 цитаты.')
        if self.weight < 1 or self.weight > 3:
            raise ValidationError("Вес цитаты должен быть в диапазоне от 1 до 3.")

    def like(self):
        self.likes += 1
        self.save(update_fields=['likes'])

    def dislike(self):
        self.dislikes += 1
        self.save(update_fields=['dislikes'])
