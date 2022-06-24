from django.urls import path

import core.views

urlpatterns = [
    path("", core.views.home, name="home")
]
