from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

import random

from app.forms.quote_add_form import QuoteAdd
from app.models.owner import Owner
from app.models.quote import Quote


class IndexView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        quotes = list(Quote.objects.all())
        quote = None
        if quotes:
            weights = [min(max(q.weight, 1), 3) for q in quotes]
            quote = random.choices(quotes, weights=weights, k=1)[0]
            quote.views += 1
            quote.save(update_fields=['views'])
        return render(request, self.template_name, {'quote': quote})


class AddQuoteView(CreateView):
    model = Quote
    form_class = QuoteAdd
    template_name = 'add_quote.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            Owner.objects.create(quote_id=self.object.id, user=self.request.user)
        return response


class EditQuoteView(UpdateView):
    model = Quote
    form_class = QuoteAdd
    template_name = 'edit_quote.html'
    success_url = reverse_lazy('index')


class LikeQuoteView(View):
    def post(self, request, quote_id, *args, **kwargs):
        quote = get_object_or_404(Quote, pk=quote_id)
        quote.like()
        return redirect('index')


class DislikeQuoteView(View):
    def post(self, request, quote_id, *args, **kwargs):
        quote = get_object_or_404(Quote, pk=quote_id)
        quote.dislike()
        return redirect('index')
