import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    class Meta:
        model = User
        fields = ["name", "surname", "email", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")


class UserProfileForm(forms.ModelForm):
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone:
            if phone.startswith("8"):
                phone = "+7" + phone[1:]
            elif not phone.startswith("+7"):
                raise ValidationError(
                    "Телефон должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX"
                )

            if not re.match(r"^\+7\d{10}$", phone):
                raise ValidationError("Телефон должен содержать 10 цифр после +7")

            if User.objects.exclude(pk=self.instance.pk).filter(phone=phone).exists():
                raise ValidationError("Пользователь с таким телефоном уже существует")
        return phone

    def clean_github_url(self):
        url = self.cleaned_data.get("github_url")
        if url and "github.com" not in url:
            raise ValidationError("Ссылка должна вести на GitHub")
        return url

    class Meta:
        model = User
        fields = ["name", "surname", "avatar", "about", "phone", "github_url"]
