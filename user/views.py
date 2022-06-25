from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView

# Create your views here.
from django.shortcuts import render, redirect
from django.views import View

from user.forms import LoginForm


class UserLoginView(LoginView):
    """Вход на сайт"""
    template_name = "user/login.html"
    authentication_form = LoginForm


class UserRegisterView(View):
    """Регистрация на сайте"""
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, "user/register.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Вы успешно зарегистрировались!")
            return redirect("home")
        else:
            return render(request, "user/register.html", context={"form": form})
