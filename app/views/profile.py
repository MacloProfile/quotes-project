from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from app.models.quote import Quote


class ProfileView(LoginRequiredMixin, ListView):
    model = Quote
    template_name = 'profile.html'
    context_object_name = 'quotes'
    paginate_by = 9  # 3 на 3

    def get_queryset(self):
        # Получаем цитаты текущего пользователя
        return Quote.objects.filter(owner__user=self.request.user).order_by('-id')
