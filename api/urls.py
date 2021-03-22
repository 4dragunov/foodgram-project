from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (FavoriteView, IngredientsViewSet, PurchaseView,
                    SubscribeView)

v1_patterns = (
    [
        path("subscriptions/", SubscribeView.as_view(), name="add_follow"),
        path("subscriptions/<int:author_id>/", SubscribeView.as_view(),
             name="delete_follow",
             ),
        path("purchases/", PurchaseView.as_view(), name="add_purchase"),
        path("purchases/<int:recipe_id>/", PurchaseView.as_view(),
             name="delete_purchase",
             ),
        path("favorites/", FavoriteView.as_view(), name="add_favorite"),
        path("favorites/<int:recipe_id>/", FavoriteView.as_view(),
             name="delete_favorite",
             ),
    ]
)

v1_router = DefaultRouter()

v1_router.register(r'ingredients', IngredientsViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include(v1_patterns)),

]
