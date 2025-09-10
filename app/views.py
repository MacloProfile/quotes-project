from django.shortcuts import render
from .models import Quote
import random


def index(request):
    quotes = list(Quote.objects.all())
    quote = None

    if quotes:
        weights = [q.weight for q in quotes]

        quote = random.choices(quotes, weights=weights, k=1)[0]

        quote.views += 1
        quote.save()

    return render(request, 'index.html', {'quote': quote})


def top_quotes(request):
    top = Quote.objects.order_by('-likes')[:10]
    return render(request, 'top.html', {'top_quotes': top})
