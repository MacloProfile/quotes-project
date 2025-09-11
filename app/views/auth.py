from django.views.generic import CreateView
from django.urls import reverse_lazy

from app.forms.user_registration_form import CustomUserCreationForm


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
