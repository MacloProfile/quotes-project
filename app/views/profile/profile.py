from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from app.models.quote import Quote


class ProfileView(LoginRequiredMixin, ListView):
    model = Quote
    template_name = 'profile/profile.html'
    context_object_name = 'quotes'
    paginate_by = 9

    def get_queryset(self):
        return Quote.objects.filter(owner__user=self.request.user).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.user.email
        context['username'] = self.request.user.username
        context['last_activity'] = self.request.user.last_login
        return context
