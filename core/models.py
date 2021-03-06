from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


class Ingredient(models.Model):
    """Ингредиент"""
    name = models.CharField(unique=True, max_length=150, blank=False, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="Slug")

    def get_absolute_url(self):
        return reverse("recipe_ingredient", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"


class Recipe(models.Model):
    """Рецепт"""
    title = models.CharField(max_length=150, blank=False, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    content = RichTextUploadingField(blank=True, null=True, verbose_name="Рецепт")
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient", related_name="recipes",
                                         verbose_name="Ингредиенты")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes", verbose_name="Пользователь")
    image = models.ImageField(upload_to="recipe_images", verbose_name="Изображение", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")
    favorited_by = models.ManyToManyField(User, related_name="favorite_recipes", verbose_name="Избран пользователями")
    views = models.PositiveIntegerField(default=1, verbose_name="Количество просмотров")

    def get_absolute_url(self):
        return reverse("recipe_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class RecipeIngredient(models.Model):
    """Ингредиент рецепта"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Ингредиент")
    quantity = models.IntegerField(verbose_name="Количество")
    unit = models.CharField(max_length=10, verbose_name="Единица измерения")

    def __str__(self):
        return self.recipe.title + " " + self.ingredient.name

    class Meta:
        verbose_name = "Ингредиент рецепта"
        verbose_name_plural = "Ингредиенты рецептов"


class Comment(models.Model):
    """Комментарий рецепта"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name="comments")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт", related_name="comments")
    text = RichTextField(verbose_name="Текст комментария")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name="Родительский комментарий", null=True,
                               blank=True, related_name="replies")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")

    def __str__(self):
        return f"{self.recipe.title} ({self.user.username} {self.created_at})"

    class Meta:
        verbose_name = "Комментарий рецепта"
        verbose_name_plural = "Комментарии рецептов"
