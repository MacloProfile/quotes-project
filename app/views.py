from django.shortcuts import render, redirect, get_object_or_404

from .forms import QuoteAdd
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


def add_quote(request):
    if request.method == 'POST':
        form = QuoteAdd(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = QuoteAdd()
    return render(request, 'add_quote.html', {'form': form})


def like_quote(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    quote.like()
    return redirect('index')


def dislike_quote(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    quote.dislike()
    return redirect('index')

