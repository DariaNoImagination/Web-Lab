from django.shortcuts import render

def index(request):

    data = {
        'title': 'Сообщества фанатов',
    }
    return render(request, 'information.html',
                  context=data)


