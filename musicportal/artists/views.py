from django.shortcuts import render, redirect
from data import genres_data,all_artist_data
def index(request):
    data = {
        'title': 'Музыкальные исполнители',
        'posts': all_artist_data,
    }
    return render(request, 'information.html',
                  context=data)


def categories(request): #Жанры
    data = {
        'title': 'Жанры',
        'categories': genres_data,
        'app_name': 'artists'
    }
    return render(request, 'categories.html',
                  context=data)


def artists_by_genre(request, genre_slug):
    genre_names = {
        'pop': 'поп',
        'rock': 'рок',
        'rnb': 'R&B',
    }
    if genre_slug not in genre_names:
        return redirect('all_artists')

    filtered_artists = [artist for artist in all_artist_data if artist['genre'] == genre_slug]

    genre_name = genre_names[genre_slug]
    data = {
        'title': f'Исполнители жанра {genre_name}',
        'posts': filtered_artists,
    }
    return render(request, 'information.html', context=data)



