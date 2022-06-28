from django.contrib.auth.views import LogoutView
from django.urls import path

from user.views import UserLoginView, UserRegisterView, UserDetailView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("info/<slug:username>/", UserDetailView.as_view(), name="user_info"),
]
