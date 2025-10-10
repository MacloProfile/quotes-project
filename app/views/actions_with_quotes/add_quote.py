from django.views.generic import CreateView
from django.urls import reverse_lazy
from app.tasks.check_new_quote import moderate_quote_task


from app.forms.quote_add_form import QuoteAdd
from app.models.owner import Owner
from app.models.quote import Quote


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
