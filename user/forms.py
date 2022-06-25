from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
import django.forms as forms


class LoginForm(AuthenticationForm):
    """Форма входа"""
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"}))
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "class": "form-control"}),
    )
