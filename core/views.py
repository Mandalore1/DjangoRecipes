from django.contrib import messages
from django.shortcuts import render

from django.views.generic import DetailView, ListView

from core.models import Recipe, RecipeIngredient


def home(request):
    """Главная страница"""
    return render(request, "home.html")


class RecipeDetailView(DetailView):
    """Информация о рецепте"""
    model = Recipe
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ingredients = RecipeIngredient.objects.filter(recipe=self.object).select_related("ingredient")
        context["ingredients"] = ingredients
        return context


class RecipeListView(ListView):
    """Список рецептов"""
    model = Recipe
    queryset = Recipe.objects.filter(is_published=True)
    context_object_name = "recipes"
