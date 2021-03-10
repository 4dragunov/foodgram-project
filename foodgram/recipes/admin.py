from django.contrib import admin

from .models import (Favorite, Ingredients, Ingredients_for_recipe, Purchase,
                     Recipe, Subscription)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_filter = ("title",)
    empty_value_display = "-пусто-"


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_filter = ("title",)
    empty_value_display = "-пусто-"


admin.site.register(Ingredients_for_recipe)
admin.site.register(Subscription)
admin.site.register(Favorite)
admin.site.register(Purchase)
