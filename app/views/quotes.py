import json

from django.shortcuts import render
from django.views import View

import random

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
