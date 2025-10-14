from django import forms
from django.contrib.auth import password_validation


class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField(label="Новый email", required=True)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Старый пароль", widget=forms.PasswordInput, required=True
    )
    new_password = forms.CharField(
        label="Новый пароль", widget=forms.PasswordInput, required=True
    )
    confirm_password = forms.CharField(
        label="Подтверждение пароля", widget=forms.PasswordInput, required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")
        password_validation.validate_password(new_password)
        return cleaned_data
