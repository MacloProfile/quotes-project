from django.conf import settings
from django.db import models

from app.models.quote import Quote


class Owner(models.Model):
    quote = models.OneToOneField(Quote, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
