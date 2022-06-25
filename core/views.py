from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.db import DatabaseError

from django.views.generic import DetailView, ListView, CreateView, UpdateView

from core.forms import RecipeCreationForm, RecipeForm
from core.models import Recipe, RecipeIngredient, Ingredient


def _add_ingredients_to_context(context, recipe):
    """Добавляем в контекст ингредиенты рецепта"""
    ingredients = RecipeIngredient.objects.filter(recipe=recipe).select_related("ingredient")
    context["ingredients"] = ingredients
    return context


def home(request):
    """Главная страница"""
    return render(request, "home.html")


class RecipeDetailView(DetailView):
    """Информация о рецепте"""
    model = Recipe
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        """Добавляем в контекст ингредиенты рецепта"""
        context = super().get_context_data(**kwargs)
        return _add_ingredients_to_context(context, self.object)


class RecipeListView(ListView):
    """Список рецептов"""
    model = Recipe
    queryset = Recipe.objects.filter(is_published=True)
    context_object_name = "recipes"


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """Начальное создание рецепта"""
    model = Recipe
    template_name_suffix = "_create"
    form_class = RecipeCreationForm

    def form_valid(self, form):
        """Устанавливаем пользователя рецепта перед сохранением"""
        form.instance.user = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Обновление данных рецепта"""
    model = Recipe
    template_name_suffix = "_update"
    form_class = RecipeForm
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        """Добавляем в контекст ингредиенты рецепта"""
        context = super().get_context_data(**kwargs)
        return _add_ingredients_to_context(context, self.object)

    def test_func(self):
        """Тестирует, что пользователь в запросе тот же, что и владелец рецепта"""
        return self.request.user == self.get_object().user


@login_required
def recipe_publish(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user != recipe.user:
        return HttpResponseForbidden()

    recipe.is_published = True
    recipe.save()
    messages.success(request, "Рецепт успешно опубликован")
    return redirect("recipe_detail", pk=pk)


@login_required
def add_ingredient(request, pk):
    if request.method != "POST":
        return HttpResponseBadRequest

    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user != recipe.user:
        return HttpResponseForbidden()

    name = request.POST["name"]
    quantity = request.POST["quantity"]
    unit = request.POST["unit"]

    try:
        ingredient = Ingredient.objects.filter(name=name)
        if ingredient.exists():
            ingredient = ingredient[0]
        else:
            slug = slugify(name, allow_unicode=True)
            ingredient = Ingredient.objects.create(name=name, slug=slug)
        recipe_ingredient = RecipeIngredient(ingredient=ingredient, recipe=recipe, quantity=quantity, unit=unit)
        recipe_ingredient.save()
    except DatabaseError:
        messages.error(request, "Не удалось добавить ингредиент!")

    return redirect("recipe_update", pk=recipe.pk)


@login_required
def delete_ingredient(request, pk):
    ingredient = get_object_or_404(RecipeIngredient, pk=pk)
    recipe = ingredient.recipe
    if request.user != recipe.user:
        return HttpResponseForbidden()

    ingredient.delete()

    return redirect("recipe_update", pk=recipe.pk)
