from django.urls import path

import core.views

urlpatterns = [
    path("", core.views.home, name="home"),
    path("recipe/<int:pk>/", core.views.RecipeView.as_view(), name="recipe_detail")
]
