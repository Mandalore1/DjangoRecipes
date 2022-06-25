import django.forms as forms

from core.models import Recipe


class RecipeCreationForm(forms.ModelForm):
    """Форма для начального создания рецепта"""
    class Meta:
        model = Recipe
        fields = ("title", "description")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"})
        }
