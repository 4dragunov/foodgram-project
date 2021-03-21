from django import forms
from django.core.exceptions import ValidationError
from .models import Recipe, Ingredients, IngredientsForRecipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'tags', 'prep_time', 'description', 'image')

