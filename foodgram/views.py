from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, 'misc/404.html')


def server_error(request):
    return render(request, 'misc/500.html')
