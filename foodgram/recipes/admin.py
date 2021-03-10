from django.contrib import admin

from .models import (Favorite, Ingredients, Ingredients_for_recipe, Purchase,
                     Recipe, Subscription)

admin.site.register(Recipe)
admin.site.register(Ingredients)
admin.site.register(Ingredients_for_recipe)
admin.site.register(Subscription)
admin.site.register(Favorite)
admin.site.register(Purchase)
