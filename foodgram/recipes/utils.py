from django import template
from django.core.paginator import Paginator

register = template.Library()


def get_ingridient_from_form(QueryDict):
    '''
    Функция принимает на вход QueryDict POST запроса, парсит новые
    ингридиенты для рецепта и возвращает список ингридиентов, состоящий
    названия и количества
    '''
    print(QueryDict)
    count = 0
    for key in QueryDict.keys():
        if 'nameIngredient_' in key:
            count += 1
    ing = []
    for number in range(1, count + 1):
        number = str(number)
        nameIngredient = 'nameIngredient_' + str(number)
        valueIngredient = 'valueIngredient_' + str(number)
        ing.append([QueryDict[nameIngredient], QueryDict[
            valueIngredient]])

    return (ing)


def get_tags_url(request):
    '''Получение списка тегов из URL GET запроса'''
    tags = request.GET.getlist('tag')
    return tags


def paginator_data(request, recipies, count=6):
    '''Пагинация'''
    paginator = Paginator(recipies, count)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page, paginator
