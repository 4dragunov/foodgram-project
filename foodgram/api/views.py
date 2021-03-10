from recipes.models import (Favorite, Ingredients, Purchase, Recipe,
                            Subscription, User)

from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly
from .serializers import (FavoriteSerializer, IngredientsSerializer,
                          PurchaseSerializer, SubscriptionSerializer)


class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        """создание подписки на автора."""
        author_id = int(self.request.data.get('id'))
        author = get_object_or_404(User, id=author_id)
        serializer.save(user=self.request.user, author=author)

    def destroy(self, request, *args, **kwargs):
        """удаление подписки на автора."""
        subscription = get_object_or_404(Subscription,
                                         author_id=kwargs.get('pk'),
                                         user=request.user)
        self.perform_destroy(subscription)
        return Response({"success": True})


class IngredientsViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()

    def list(self, request, *args, **kwargs):
        """вывод списка ингридиентов"""
        query = request.GET['query']
        queryset = self.queryset.filter(title__contains=query)
        serializer = IngredientsSerializer(queryset, many=True)
        return Response(serializer.data)


class FavoriteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        """добавление рецепта из избранного"""
        recipe_id = int(self.request.data.get('id'))
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer.save(user=self.request.user, recipe=recipe)

    def destroy(self, request, *args, **kwargs):
        """удаление рецепта из избранного"""
        favorite_recipe = get_object_or_404(Favorite,
                                            recipe_id=kwargs.get('pk'),
                                            user=request.user)
        self.perform_destroy(favorite_recipe)
        return Response({"success": True})


class PurchaseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def perform_create(self, serializer):
        """добавление рецепта в список покупок"""
        recipe_id = int(self.request.data.get('id'))
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer.save(user=self.request.user, recipe=recipe)

    def destroy(self, request, *args, **kwargs):
        """удаление рецепта из списка покупок"""
        purchase_recipe = get_object_or_404(Purchase,
                                            recipe_id=kwargs.get('pk'),
                                            user=request.user)
        self.perform_destroy(purchase_recipe)
        return Response({"success": True})
