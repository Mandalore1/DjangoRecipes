from django.urls import path

import core.views

urlpatterns = [
    path("", core.views.home, name="home"),
    path("recipes/", core.views.RecipeListView.as_view(), name="recipe_list"),
    path("recipes/create/", core.views.RecipeCreateView.as_view(), name="recipe_create"),
    path("recipes/<int:pk>/", core.views.RecipeDetailView.as_view(), name="recipe_detail"),
    path("recipes/<int:pk>/update", core.views.RecipeUpdateView.as_view(), name="recipe_update"),
    path("recipes/<int:pk>/publish", core.views.recipe_publish, name="recipe_publish"),
]
