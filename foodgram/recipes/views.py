import operator
from functools import reduce

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.views.generic import View
from django.views.generic.base import TemplateView

from .forms import RecipeForm
from .models import Ingredients, Ingredients_for_recipe, Recipe, Subscription, \
    Purchase
from .utils import get_ingridient_from_form, paginator_data

User = get_user_model()


def index(request):
    '''Вьюха отображения главной страницы'''
    # получаем список тегов из GET запроса
    tags = request.GET.getlist('tag')
    if tags:
        # фильтрация по совокупности выбранных тегов
        query = reduce(operator.or_, (Q(tags__contains=tag) for tag in tags))
        recipies = Recipe.objects.filter(query).order_by('-date_pub')
    else:
        recipies = Recipe.objects.all().order_by('-date_pub')
    # Т.к. паджинатор есть почти на каждой странице - вынес некоторые моменты
    # в отдельную функцию в utils.py
    page, paginator = paginator_data(request, recipies)

    return render(request, 'index.html', context={'page': page,
                                                  'paginator': paginator,
                                                  'tags': tags})


def recipe_detail(request, slug):
    '''Вьюха отображения страницы рецепта'''
    recipe = get_object_or_404(Recipe, slug__iexact=slug)
    return render(request, 'recipe_detail.html', context={'recipe': recipe})


def profile_index(request, username):
    '''Персональная страница пользователя'''
    author = get_object_or_404(User, username=username)
    user = request.user
    recipies = author.recipes.all()

    following = Subscription.objects.filter(user__username=user,
                                            author=author).count()
    return render(request, 'profile.html', context={'recipies': recipies,
                                                    'author': author,
                                                    'user': user,
                                                    'following': following})


@login_required
def subscription_index(request):
    '''Страница подписок пользователя'''
    follow_authors = User.objects.filter(
        following__user=request.user).prefetch_related('recipes')
    page, paginator = paginator_data(request, follow_authors)
    return render(request, 'subscription_index.html',
                  context={'page': page, 'paginator': paginator, })


@login_required
def favorite_index(request):
    '''Страница подписок пользователя'''
    tags = request.GET.getlist('tag')
    if tags:
        # фильтрация по совокупности выбранных тегов
        query = reduce(operator.or_, (Q(tags__contains=tag) for tag in tags))
        recipies = Recipe.objects.filter(query).order_by('-date_pub').filter(
            favorites__user=request.user).select_related('author')
    else:
        recipies = Recipe.objects.all().order_by('-date_pub').filter(
            favorites__user=request.user).select_related('author')

    page, paginator = paginator_data(request, recipies)

    return render(request, 'favorite_index.html',
                  context={'page': page,
                           'paginator': paginator,
                           'tags': tags})


@login_required
def purchase_index(request):
    '''Список покупок'''
    recipies = Recipe.objects.filter(
        purchases__user=request.user)
    return render(request, 'purchase_index.html', context={
        'recipies': recipies})


@login_required
def get_purchase_list(request):
    '''Скачивание файла со списком покупок'''
    # recipies = Recipe.objects.filter(
    #     purchases__user=request.user)
    #
    # file_name = 'Purchase_list.txt'
    # txt = ''
    # purchase_dict = {}
    # for recipe in recipies:
    #
    #     for title, amount, dimension in recipe.ingredients:
    #         if title in purchase_dict.keys():
    #             purchase_dict[title][0] += amount
    #         else:
    #             purchase_dict[title] = [amount, dimension]
    #
    # for title, detail in purchase_dict.items():
    #     txt += (f'{title}: {detail[0]} {detail[1]}\n')



    pass
    # recipies = Recipe.objects.filter(
    #         purchases__user=request.user).ingridients
    # print(recipies)
    # ingredients = recipies.values('ingridients')
    #     # 'recipe__recipe_ingredient',)
    # print(ingredients)
        # 'recipe__dimension')
    # ).annotate(total_quantity=Sum('recipe__recipeingredient__quantity'
    #     )
    # )
    # content = ""
    # for ingredient in ingredients:
    #     item = (f'{ingredient["recipe__ingredients__title"]} '
    #             f'{ingredient["total_quantity"]} '
    #             f'{ingredient["recipe__ingredients__dimension"]}')
    #     content += item + '\n'

    # ingredients = cart.values(
    #     'recipe__ingredients__title',
    #     'recipe__ingredients__dimension'



    # response = HttpResponse(txt, content_type='application/text charset=utf-8')
    # response['Content-Disposition'] = f'attachment; filename={file_name}'
    # return response


class RecipeCreateUpdate(View):
    '''Создание или редактирование рецепта'''

    def get(self, request, slug=None):
        if slug:
            recipe = get_object_or_404(Recipe,
                                       author__username=self.request.user.username,
                                       slug__iexact=slug)
            form = RecipeForm(instance=recipe)
            title = 'Редактирование рецепта'
            botton_name = 'Изменить рецепт'
            context = {
                'form': form,
                'botton_name': botton_name,
                'title': title,
                'recipe': recipe,
            }
        else:
            form = RecipeForm()
            title = 'Создание рецепта'
            botton_name = 'Создать рецепт'
            context = {
                'form': form,
                'botton_name': botton_name,
                'title': title
            }
        template = 'recipe_create_or_update.html'
        return render(request, template, context)

    def post(self, request, slug=None):
        if slug:
            recipe = get_object_or_404(Recipe,
                                       author__username=self.request.user.username,
                                       slug__iexact=slug)
            bound_form = RecipeForm(request.POST, files=request.FILES,
                                    instance=recipe)

        else:
            bound_form = RecipeForm(request.POST, files=request.FILES)

        if bound_form.is_valid():
            new_recipe = bound_form.save(commit=False)
            new_recipe.tags = request.POST.getlist('tags')
            new_recipe.author = request.user
            new_recipe.save()
            # вытаскиваем список ингридиентов из формы
            ingridients_list = get_ingridient_from_form(request.POST)
            for ingridient_item in ingridients_list:
                ingredient = get_object_or_404(Ingredients,
                                               title=ingridient_item[0])
                amount = ingridient_item[1]
                Ingredients_for_recipe.objects.create(recipe=new_recipe,
                                                      ingredient=ingredient,
                                                      amount=amount)

            return redirect(new_recipe)
        return render(request, 'recipe_create_or_update.html',
                      context={'form': bound_form})


class RecipeDelete(View):
    '''Удаление рецепта'''

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, author=request.user, id=pk)
        recipe.delete()
        return redirect('index')


class About(TemplateView):
    '''Об авторе'''
    template_name = 'about.html'


class Technologies(TemplateView):
    '''Технологии'''
    template_name = 'technologies.html'
