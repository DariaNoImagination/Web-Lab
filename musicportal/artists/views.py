from django.shortcuts import render, get_object_or_404
from artists.models import Artist,Genre
def index(request):
    data = {
        'title': 'Музыкальные исполнители',
        'posts': Artist.objects.all(),
    }
    return render(request, 'information.html',
                  context=data)


def categories(request):  # Жанры
    genres = Genre.objects.all()
    data = {
        'title': 'Жанры',
        'categories': genres,
        'app_name': 'artists'
    }
    return render(request, 'categories.html', context=data)


def artists_by_genre(request, genre_slug):
    genre = get_object_or_404(Genre, slug=genre_slug)
    artists = Artist.objects.filter(genre=genre_slug)

    data = {
        'title': f'Исполнители жанра {genre.title}',
        'posts': artists,
        'app_name': 'artists'
    }
    return render(request, 'information.html', context=data)



