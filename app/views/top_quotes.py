from django.views.generic import ListView

from app.constants import QUOTE_SORT_VARIANTS
from app.models.quote import Quote


class TopQuotesView(ListView):
    model = Quote
    template_name = 'top.html'
    context_object_name = 'top_quotes'

    def get_queryset(self):
        sort = self.request.GET.get('sort', '-likes')
        sort_result = QUOTE_SORT_VARIANTS.get(sort, '-likes')
        return Quote.objects.order_by(sort_result)[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', 'likes')
        return context
