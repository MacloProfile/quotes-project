from django.shortcuts import redirect
from django.views.generic import CreateView

from app.forms.quote_add_form import QuoteAdd
from app.models.quote import Quote
from app.models.owner import Owner
from app.tasks.check_new_quote import moderate_quote_task


class AddQuoteView(CreateView):
    model = Quote
    form_class = QuoteAdd
    template_name = 'add_quote.html'

    def form_valid(self, form):
        self.object = form.save()
        if self.request.user.is_authenticated:
            Owner.objects.create(quote_id=self.object.id, user=self.request.user)

        moderate_quote_task.delay(self.object.id)
        return redirect('quote_added', pk=self.object.pk)
