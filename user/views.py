from django.db.models import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView

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


class UserDetailView(DetailView):
    """Информация о пользователе"""
    slug_url_kwarg = "username"
    slug_field = "username"
    model = User
    context_object_name = "user"
    template_name = "user/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["additional_info"] = self.object.additional_info
        except ObjectDoesNotExist:
            context["additional_info"] = None
        return context
