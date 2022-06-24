from django.urls import path

import core.views

urlpatterns = [
    path("", core.views.home, name="home"),
    path("recipes/", core.views.RecipeListView.as_view(), name="recipe_list"),
    path("recipes/<int:pk>/", core.views.RecipeDetailView.as_view(), name="recipe_detail"),
]
