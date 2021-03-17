from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from recipes.models import (Favorite, Ingredients, Purchase,
                            Subscription, User)

from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import IngredientsSerializer
from .utils import PurchaseFavoriteMixin


class PurchaseView(APIView, PurchaseFavoriteMixin):
    '''Список покупок - добавление и удаление'''
    model = Purchase


class FavoriteView(APIView, PurchaseFavoriteMixin):
    '''Список избранных рецептов - добавление и удаление'''
    model = Favorite


class SubscribeView(LoginRequiredMixin, APIView):
    '''Создание и удаление подписок на авторов'''

    def post(self, request):
        '''Подписка'''
        author_id = int(self.request.data.get('id'))
        if author_id:
            author = get_object_or_404(User, id=author_id)
            Subscription.objects.get_or_create(user=self.request.user,
                                               author=author)
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": "false",
                                 "message": "id not found"},
                                status=400)

    def delete(self, request, author_id):
        '''Удаление подписки на автора'''
        Subscription.objects.filter(
            user=self.request.user, author=author_id).delete()
        return JsonResponse({"success": True})


class IngredientsViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()

    def list(self, request, *args, **kwargs):
        """вывод списка ингридиентов"""
        query = request.GET['query']
        queryset = self.queryset.filter(title__contains=query)
        serializer = IngredientsSerializer(queryset, many=True)
        return Response(serializer.data)
