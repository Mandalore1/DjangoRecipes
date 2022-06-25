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


class RecipeForm(forms.ModelForm):
    """Форма рецепта"""
    class Meta:
        model = Recipe
        fields = ("title", "description", "content", "image", "is_published")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"})
        }
