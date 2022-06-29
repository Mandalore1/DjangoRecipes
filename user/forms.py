from django.contrib.auth.forms import AuthenticationForm, UsernameField
import django.forms as forms
from django.contrib.auth.models import User

from user.models import UserAdditionalInfo


class LoginForm(AuthenticationForm):
    """Форма входа"""
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"}))
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "class": "form-control"}),
    )


class UserMainInfoForm(forms.ModelForm):
    """Форма редактирования основной информации"""
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class UserAdditionalInfoForm(forms.ModelForm):
    """Форма редактирования дополнительной информации"""
    class Meta:
        model = UserAdditionalInfo
        fields = ("avatar", "about", "date_of_birth", "place")
        widgets = {
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "about": forms.Textarea(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(attrs={"class": "form-control"}),
            "place": forms.TextInput(attrs={"class": "form-control"}),
        }
