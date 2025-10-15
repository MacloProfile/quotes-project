from django.views.generic import DetailView
from app.models.quote import Quote


class QuoteAddedView(DetailView):
    model = Quote
    template_name = 'quote_added.html'
    context_object_name = 'quote'
