from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import Ingredients, IngredientsForRecipe, Recipe


class RecipeForm(forms.ModelForm):
    prep_time = forms.IntegerField(
        min_value=1,
        required=True,
    )

    class Meta:
        model = Recipe
        fields = ('title', 'tags', 'prep_time', 'description', 'image')

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['tags'].error_messages = {
            'required': 'Выберите хотя бы один тег'}

    def clean_ingridient(self):
        super().clean()
        new_ingridients_list = {}
        for key, title in self.data.items():
            if 'nameIngredient_' in key:
                elem = key.split("_")
                new_ingridients_list[title] = int(self.data[f'valueIngredient'
                                                            f'_{elem[1]}'])

        ing_titles = self.data.getlist("nameIngredient")
        ing_amount = self.data.getlist("valueIngredient")

        for title, amount in new_ingridients_list.items():
            ing_titles.append(title)
            ing_amount.append(amount)

        clean_items = {}
        for number, item in enumerate(ing_titles):
            ingridient = get_object_or_404(Ingredients, title=item)
            clean_items[ingridient] = ing_amount[number]
        self.cleaned_data['items'] = clean_items
        return self.cleaned_data['items']

    def clean(self):
        ingridients = self.clean_ingridient()

        if len(ingridients) == 0:
            raise ValidationError(
                'Из ничего вкусно не получится! Добавьте что-нибудь',
            )

        for value in ingridients.values():
            if int(value) < 1:
                raise ValidationError(
                    'Уберите ингридиент с 0 значением',
                )

    def save(self, commit=True):
        request = self.initial["request"]
        recipe = super().save(commit=False)
        recipe.author = request.user
        recipe.save()
        self.save_m2m()
        new_ingredients = self.clean_ingridient()
        recipe_ingredients = IngredientsForRecipe.objects.filter(
            recipe=self.instance)
        recipe_ingredients.delete()
        for ingredient, amount in new_ingredients.items():
            IngredientsForRecipe.objects.update_or_create(
                recipe=self.instance,
                ingredient=ingredient,
                amount=amount)
        return self.instance
