from django.urls import path

import core.views

urlpatterns = [
    path("test/", core.views.test)
]
