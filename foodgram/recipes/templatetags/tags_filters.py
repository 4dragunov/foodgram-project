from django import template

register = template.Library()


@register.simple_tag
def set_tags_url(request, tag):
    request_copy = request.GET.copy()
    tags = request_copy.getlist('tag')
    if tag in tags:
        tags.remove(tag)
    else:
        tags.append(tag)
    request_copy.setlist('tag', tags)
    return request_copy.urlencode()


@register.simple_tag
def set_tags_page_url(request, page):
    request_copy = request.GET.copy()
    request_copy['page'] = page
    return request_copy.urlencode()
