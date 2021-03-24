from django import template

from recipes.models import Favorite, Purchase, Subscription

register = template.Library()


@register.filter
def check_subscribe(author, user):
    '''Проверка наличия подписки пользователя на автора рецепта'''
    return Subscription.objects.filter(author_id=author.id,
                                       user_id=user.id).exists()


@register.filter
def check_favorite(recipe, user):
    '''Проверка наличия рецепта в избранном у пользователя'''
    return Favorite.objects.filter(recipe_id=recipe.id,
                                   user_id=user.id).exists()


@register.filter
def check_purchase(recipe, user):
    '''Проверка наличия рецепта в избранном у пользователя'''
    return Purchase.objects.filter(recipe_id=recipe.id,
                                   user_id=user.id).exists()


@register.filter(name='count_purchase')
def count_purchase(user):
    '''Подсчет количества рецептов в списке покупок'''
    return Purchase.objects.filter(user_id=user.id).count()
