from django.contrib import messages
from django.shortcuts import render

from django.views.generic import DetailView

from core.models import Recipe


def home(request):
    return render(request, "home.html")


class RecipeView(DetailView):
    model = Recipe
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ingredients = self.object.ingredients.through.objects.all().select_related("ingredient")
        context["ingredients"] = ingredients
        return context

