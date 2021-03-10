from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (FavoriteViewSet, IngredientsViewSet,
                    PurchaseViewSet, SubscriptionViewSet)

router = DefaultRouter()

router.register(r'favorites', FavoriteViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'ingredients', IngredientsViewSet)
router.register(r'subscriptions', SubscriptionViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]
