from django.contrib import admin

# Register your models here.
from core.models import Recipe, Ingredient, RecipeIngredient


class IngredientAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Recipe)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient)
