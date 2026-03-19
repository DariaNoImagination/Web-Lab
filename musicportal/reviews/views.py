from django.shortcuts import render, redirect
from data import reviews_data,genres_data
def index(request):
    data = {
        'title': 'Рецензии',
        'posts': reviews_data
    }
    return render(request, 'information.html',
                  context=data)

def categories(request): #Жанры
    data = {
        'title': 'Рецензии по жанрам',
        'categories': genres_data,
        'app_name': 'reviews'
    }
    return render(request, 'categories.html',
                  context=data)

def reviews_by_genre(request, genre_slug):
    genre_names = {
        'pop': 'поп',
        'rock': 'рок',
        'rnb': 'R&B',
    }
    if genre_slug not in genre_names:
        return redirect('all_reviews')

    filtered_reviews = [review for review in reviews_data if review['genre'] == genre_slug]


    genre_name = genre_names[genre_slug]

    data = {
        'title': f'Рецензии жанра {genre_name}',
        'posts': filtered_reviews,
    }

    return render(request, 'information.html', context=data)