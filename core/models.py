from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Ingredient(models.Model):
    name = models.CharField(unique=True, max_length=150, blank=False, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="Slug")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"


class Recipe(models.Model):
    title = models.CharField(max_length=150, blank=False, verbose_name="Название")
    content = models.TextField(blank=True, null=True, verbose_name="Рецепт")
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient", related_name="recipes",
                                         verbose_name="Ингредиенты")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes", verbose_name="Пользователь")
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Ингредиент")
    quantity = models.IntegerField(verbose_name="Количество")
    unit = models.CharField(max_length=10, verbose_name="Единица измерения")

    def __str__(self):
        return self.recipe.title + " " + self.ingredient.name

    class Meta:
        verbose_name = "Ингредиент рецепта"
        verbose_name_plural = "Ингредиенты рецептов"
