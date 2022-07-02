from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.db import DatabaseError
from django.views import View

from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

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

    def get_object(self, *args, **kwargs):
        """Увеличиваем счетчик просмотров на 1 и добавляем индикатор добавления в избранное"""
        recipe = super().get_object(*args, **kwargs)
        recipe.views += 1
        recipe.save(update_fields=["views"])

        recipe.is_favorite = recipe.favorited_by.filter(pk=self.request.user.pk).exists()

        return recipe

    def get_context_data(self, **kwargs):
        """Добавляем в контекст ингредиенты рецепта"""
        context = super().get_context_data(**kwargs)
        return _add_ingredients_to_context(context, self.object)


class RecipeListView(ListView):
    """Список рецептов"""
    model = Recipe
    queryset = Recipe.objects.filter(is_published=True)
    context_object_name = "recipes"


class RecipeFilterView(ListView):
    """Фильтр рецептов"""
    model = Recipe
    context_object_name = "recipes"
    template_name_suffix = "_filter"

    def get_queryset(self):
        queryset = Recipe.objects.filter(is_published=True)

        if "user" in self.request.GET:
            queryset = queryset.filter(user__username=self.request.GET.get("user"))
        if "title" in self.request.GET:
            queryset = queryset.filter(title__icontains=self.request.GET.get("title"))

        return queryset


class RecipeIngredientView(ListView):
    """Рецепты по ингредиенту"""
    model = Recipe
    context_object_name = "recipes"
    template_name_suffix = "_ingredient"

    def get_queryset(self):
        ingredient = get_object_or_404(Ingredient, slug=self.kwargs.get("slug"))
        return ingredient.recipes.all()


class RecipeMyView(LoginRequiredMixin, ListView):
    """Мои рецепты"""
    model = Recipe
    context_object_name = "recipes"
    template_name_suffix = "_my"

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """Начальное создание рецепта"""
    model = Recipe
    template_name_suffix = "_create"
    form_class = RecipeCreationForm

    def form_valid(self, form):
        """Устанавливаем пользователя рецепта перед сохранением"""
        messages.success(self.request,
                         "Рецепт успешно добавлен, но еще не опубликован. Измените рецепт и опубликуйте его")
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

    def form_valid(self, form):
        messages.success(self.request, "Рецепт успешно изменен!")
        return super().form_valid(form)

    def test_func(self):
        """Тестирует, что пользователь в запросе тот же, что и владелец рецепта"""
        return self.request.user == self.get_object().user


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление рецепта"""
    model = Recipe
    context_object_name = "recipe"
    success_url = reverse_lazy("recipe_list")

    def form_valid(self, form):
        messages.success(self.request, "Рецепт успешно удален!")
        return super().form_valid(form)

    def test_func(self):
        """Тестирует, что пользователь в запросе тот же, что и владелец рецепта"""
        return self.request.user == self.get_object().user


class RecipeAddToFavorites(LoginRequiredMixin, View):
    """Добавление в избранное"""
    def post(self, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=self.kwargs["pk"])
        user = self.request.user

        # Если запись об избранном существует, удаляем ее
        if user.favorite_recipes.filter(pk=recipe.pk).exists():
            user.favorite_recipes.clear()
        # Иначе добавляем запись
        else:
            user.favorite_recipes.add(recipe)

        return redirect("recipe_detail", self.kwargs["pk"])


@login_required
def recipe_publish(request, pk):
    """Публикация рецепта"""
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user != recipe.user:
        return HttpResponseForbidden()

    recipe.is_published = True
    recipe.save()
    messages.success(request, "Рецепт успешно опубликован")
    return redirect("recipe_detail", pk=pk)


@login_required
def add_ingredient(request, pk):
    """Добавление ингредиента к рецепту"""
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
    """Удаление ингредиента рецепта"""
    ingredient = get_object_or_404(RecipeIngredient, pk=pk)
    recipe = ingredient.recipe
    if request.user != recipe.user:
        return HttpResponseForbidden()

    ingredient.delete()

    return redirect("recipe_update", pk=recipe.pk)
