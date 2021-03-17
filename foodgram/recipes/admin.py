from django.contrib import admin

from .models import (Favorite, Ingredients, IngredientsForRecipe, Purchase,
                     Recipe, Subscription)


class RecipeIngredientInline(admin.TabularInline):
    model = IngredientsForRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = ('title', 'author', 'in_favorite_count',)
    list_filter = ('title', 'author__username', 'tags')
    search_fields = ('title', 'author', 'tags')
    empty_value_display = "-пусто-"  # noqa

    def in_favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    in_favorite_count.short_description = 'Число добавлений в Избранное'


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension',)
    search_fields = ('title',)
    empty_value_display = '-пусто-'  # noqa


class IngredientsForRecipeAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", 'amount')
    list_filter = ('recipe', 'ingredient')
    empty_value_display = "-пусто-"  # noqa


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author', 'pk')
    search_fields = ('user', 'author',)
    empty_value_display = "-пусто-"  # noqa


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe',)
    empty_value_display = "-пусто-"  # noqa


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe',)
    empty_value_display = "-пусто-"  # noqa


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(IngredientsForRecipe, IngredientsForRecipeAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Purchase, PurchaseAdmin)
