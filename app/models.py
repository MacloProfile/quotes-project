from django.db import models


class Quote(models.Model):
    quote = models.TextField(unique=True)
    source = models.CharField(max_length=255)
    weight = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    created_at_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
