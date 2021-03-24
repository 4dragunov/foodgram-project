from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import (Favorite, Ingredients, Purchase, Recipe,
                            Subscription, User)
from .serializers import IngredientsSerializer


class PurchaseFavoriteMixin(APIView):
    '''Миксин пидписки и избранного (добавление и удаление)'''
    model = None
    SUCCESS_RESPONSE = JsonResponse({'success': True})

    def post(self, request):
        '''Создание'''
        recipe_id = int(self.request.data.get('id'))
        if recipe_id:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            self.model.objects.get_or_create(user=self.request.user,
                                             recipe=recipe)
        return self.SUCCESS_RESPONSE

    def delete(self, request, recipe_id):
        '''Удаление'''
        self.model.objects.filter(user=self.request.user,
                                  recipe=recipe_id).delete()
        return self.SUCCESS_RESPONSE


class PurchaseView(PurchaseFavoriteMixin):
    '''Список покупок - добавление и удаление'''
    model = Purchase


class FavoriteView(PurchaseFavoriteMixin):
    '''Список избранных рецептов - добавление и удаление'''
    model = Favorite


class SubscribeView(LoginRequiredMixin, APIView):
    '''Создание и удаление подписок на авторов'''
    SUCCESS_RESPONSE = JsonResponse({'success': True})
    BAD_RESPONSE = JsonResponse({'success': False}, status=400)

    def post(self, request):
        '''Подписка'''
        author_id = int(self.request.data.get('id'))
        if author_id:
            author = get_object_or_404(User, id=author_id)
            Subscription.objects.get_or_create(user=self.request.user,
                                               author=author)
            return self.SUCCESS_RESPONSE
        else:
            return self.BAD_RESPONSE

    def delete(self, request, author_id):
        '''Удаление подписки на автора'''
        Subscription.objects.filter(
            user=self.request.user, author=author_id).delete()
        return self.SUCCESS_RESPONSE


class IngredientsViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()

    def list(self, request, *args, **kwargs):
        """вывод списка ингридиентов"""
        query = request.GET['query']
        queryset = self.queryset.filter(title__contains=query)
        serializer = IngredientsSerializer(queryset, many=True)
        return Response(serializer.data)
