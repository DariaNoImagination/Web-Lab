from reviews.models import Review
from artists.models import Genre
from django.shortcuts import render, get_object_or_404
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
        genre=genre_slug,
    ).order_by('-rating')

    data = {
        'title': f'Рецензии жанра {genre.title}',
        'posts': reviews,
    }

    return render(request, 'information.html', context=data)