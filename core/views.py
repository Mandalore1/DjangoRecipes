from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import DetailView, ListView, CreateView, UpdateView

from core.forms import RecipeCreationForm, RecipeForm
from core.models import Recipe, RecipeIngredient


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
        ingredients = RecipeIngredient.objects.filter(recipe=self.object).select_related("ingredient")
        context["ingredients"] = ingredients
        return context


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
