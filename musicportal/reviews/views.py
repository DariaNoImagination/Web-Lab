from reviews.models import Review
from artists.models import Genre
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
def index(request):
    reviews = Review.published.all().order_by('-rating')
    data = {
        'title': 'Рецензии',
        'posts': reviews
    }
    return render(request, 'information.html',
                  context=data)

def categories(request): #Жанры
    genres = Genre.objects.all()
    data = {
        'title': 'Рецензии по жанрам',
        'categories': genres,
        'app_name': 'reviews'
    }
    return render(request, 'categories.html',
                  context=data)


def reviews_by_genre(request, genre_slug):

    genre = get_object_or_404(Genre, slug=genre_slug)

    reviews = Review.published.filter(
        Q(song__genre=genre) | Q(album__genre_id=genre)
    ).values(
        'id',
        'rating',
        'text',
        'date',
        'song__title',
        'song__artist__title',
        'album__title',
        'album__artist_id__title'
    ).order_by('-rating')

    for review in reviews:
        if review['song__title']:
            review['title'] = review['song__title']
            review['artist'] = review['song__artist__title']
        else:
            review['type'] = 'album'
            review['title'] = review['album__title']
            review['artist'] = review['album__artist_id__title']
    context = {
        'title': f'Рецензии жанра {genre.title}',
        'posts': reviews,
    }
    return render(request, 'information.html', context)