from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound,HttpResponseServerError,HttpResponseForbidden

def index(request):
    return render(request, 'main.html')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def server_error(request):
    return  HttpResponseServerError('<h1>Ошибка сервера</h1>')

def permission_denied(request, exception):
    return HttpResponseForbidden('<h1>Доступ к ресурсу запрещен</h1>')