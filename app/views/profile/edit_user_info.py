from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model

from app.forms.edit_profile_form import ChangePasswordForm, ChangeEmailForm

User = get_user_model()


class ProfileSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile_settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email_form'] = ChangeEmailForm()
        context['password_form'] = ChangePasswordForm()
        return context

    def post(self, request, *args, **kwargs):
        user = request.user

        if 'change_email' in request.POST:
            email_form = ChangeEmailForm(request.POST)
            password_form = ChangePasswordForm()
            if email_form.is_valid():
                new_email = email_form.cleaned_data['new_email']
                if User.objects.filter(email=new_email).exclude(pk=user.pk).exists():
                    messages.error(request, "Этот email уже используется.")
                else:
                    user.email = new_email
                    user.save()
                    messages.success(request, "Email успешно изменён.")
        elif 'change_password' in request.POST:
            password_form = ChangePasswordForm(request.POST)
            email_form = ChangeEmailForm()
            if password_form.is_valid():
                old_password = password_form.cleaned_data['old_password']
                new_password = password_form.cleaned_data['new_password']
                if not user.check_password(old_password):
                    messages.error(request, "Неверный старый пароль.")
                else:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, "Пароль успешно изменён.")
        else:
            email_form = ChangeEmailForm()
            password_form = ChangePasswordForm()

        return self.render_to_response({
            'email_form': email_form,
            'password_form': password_form
        })
