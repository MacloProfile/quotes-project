import json

from django.shortcuts import get_object_or_404, redirect
from django.views import View

from app.models.quote import Quote


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
