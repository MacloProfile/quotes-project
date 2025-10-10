from django.views.generic import UpdateView
from django.urls import reverse_lazy
from app.tasks.check_new_quote import moderate_quote_task

from app.forms.quote_add_form import QuoteAdd
from app.models.quote import Quote


class EditQuoteView(UpdateView):
    model = Quote
    form_class = QuoteAdd
    template_name = 'edit_quote.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.status = None
        self.object.moderation_comment = None
        self.object.save(update_fields=['status', 'moderation_comment'])

        moderate_quote_task.delay(self.object.id)
        return response
