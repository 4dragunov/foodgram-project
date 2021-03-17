from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from recipes.models import Recipe


class PurchaseFavoriteMixin:
    '''Миксин пидписки и избранного (добавление и удаление)'''
    model = None

    def post(self, request):
        '''Создание'''
        recipe_id = int(self.request.data.get('id'))
        if recipe_id:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            self.model.objects.get_or_create(user=self.request.user,
                                             recipe=recipe)
        return JsonResponse({"success": True})

    def delete(self, request, recipe_id):
        '''Удаление'''
        self.model.objects.filter(user=self.request.user,
                                  recipe=recipe_id).delete()
        return JsonResponse({"success": True})
