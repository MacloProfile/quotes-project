import json

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from app.tasks.check_new_quote import moderate_quote_task

import random

from app.forms.quote_add_form import QuoteAdd
from app.models.owner import Owner
from app.models.quote import Quote


class IndexView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        quotes = list(Quote.objects.filter(status=True))
        quote = None
        user_vote = None

        if quotes:
            weights = [min(max(q.weight, 1), 3) for q in quotes]
            quote = random.choices(quotes, weights=weights, k=1)[0]
            quote.views += 1
            quote.save(update_fields=['views'])

            voted_json = request.COOKIES.get("voted_quotes", "{}")
            try:
                voted_dict = json.loads(voted_json)
            except json.JSONDecodeError:
                voted_dict = {}

            user_vote = voted_dict.get(str(quote.id))

        return render(request, self.template_name, {
            'quote': quote,
            'user_vote': user_vote
        })


class AddQuoteView(CreateView):
    model = Quote
    form_class = QuoteAdd
    template_name = 'add_quote.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_authenticated:
            Owner.objects.create(quote_id=self.object.id, user=self.request.user)
        moderate_quote_task.delay(self.object.id)
        return response


class EditQuoteView(UpdateView):
    model = Quote
    form_class = QuoteAdd
    template_name = 'edit_quote.html'
    success_url = reverse_lazy('index')


class VoteQuoteView(View):
    def post(self, request, quote_id, vote_type, *args, **kwargs):
        quote = get_object_or_404(Quote, pk=quote_id)

        voted_json = request.COOKIES.get("voted_quotes", "{}")
        try:
            voted_dict = json.loads(voted_json)
        except json.JSONDecodeError:
            voted_dict = {}

        prev_vote = voted_dict.get(str(quote_id))

        if prev_vote == vote_type:
            return redirect(request.META.get("HTTP_REFERER", "index"))

        if prev_vote == "like":
            quote.likes = max(0, quote.likes - 1)
        elif prev_vote == "dislike":
            quote.dislikes = max(0, quote.dislikes - 1)

        if vote_type == "like":
            quote.likes += 1
        elif vote_type == "dislike":
            quote.dislikes += 1

        quote.save()

        voted_dict[str(quote_id)] = vote_type
        response = redirect(request.META.get("HTTP_REFERER", "index"))
        response.set_cookie(
            "voted_quotes",
            json.dumps(voted_dict),
            max_age=365 * 24 * 60 * 60
        )
        return response
