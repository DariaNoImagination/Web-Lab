from django.shortcuts import render
from data import songs_data,albums_data
def about_music(request):
    data = {
        'songs': songs_data,
        'albums': albums_data,
    }
    return render(request, 'music.html',
                  context=data)
