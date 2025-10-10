from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from app.models.owner import Owner
from app.models.quote import Quote


class DeleteQuoteView(DeleteView):
    model = Quote
    template_name = 'delete_quote.html'
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        quote = self.get_object()
        if request.user.is_authenticated:
            if Owner.objects.filter(quote=quote, user=request.user).exists():
                return super().dispatch(request, *args, **kwargs)
        return redirect('index')
