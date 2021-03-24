from django import template
from django.conf import settings
from django.core.paginator import Paginator

register = template.Library()


def get_tags_url(request):
    '''Получение списка тегов из URL GET запроса'''
    tags = request.GET.getlist('tag')
    return tags


def paginator_data(request, recipies):
    '''Пагинация'''
    paginator = Paginator(recipies, settings.PAG_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page, paginator
