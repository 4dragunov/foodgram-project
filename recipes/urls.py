from django.urls import path

from .views import (About, RecipeCreateUpdate, RecipeDelete, Technologies,
                    favorite_index, get_purchase_list, index, login_required,
                    profile_index, purchase_index, recipe_detail,
                    subscription_index)

urlpatterns = [
    path('', index, name='index'),
    path('about', About.as_view(), name='about_url'),
    path('technologies', Technologies.as_view(),
         name='technologies_url'),
    path('follows', subscription_index, name='user_subscription_url'),
    path('favorites', favorite_index, name='user_favorite_url'),
    path('purchases', purchase_index, name='user_purchase_url'),
    path('get_purchase_list', get_purchase_list, name='get_purchase_list_url'),
    path('user/<str:username>', profile_index, name='user_profile_url'),
    path('recipies/create', login_required(RecipeCreateUpdate.as_view()),
         name='recipe_create_url'),
    path('recipies/<str:slug>/update', login_required(
        RecipeCreateUpdate.as_view()),
         name='recipe_update_url'),
    # path('recipies/create', login_required(RecipeCreate.as_view()),
    #      name='recipe_create_url'),
    path('recipies/delete/<int:pk>', login_required(RecipeDelete.as_view()),
         name='recipe_delete_url'),
    path('recipies/<str:slug>', recipe_detail, name='recipe_detail_url'),
    # path('recipies/<str:slug>/update', RecipeUpdate.as_view(),
    #      name='recipe_update_url'),
]
