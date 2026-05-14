from reviews.models import Review, Comment
from artists.models import Genre
from django.shortcuts import render, get_object_or_404,redirect

from django.db.models import Q
from .forms import AddCommentForm,AddReviewForm
def index(request):
    reviews = Review.published.all().order_by('-rating')
    data = {
        'title': 'Рецензии',
        'posts': reviews
    }
    for review in reviews:
        review.comments_list = review.comments.filter(is_published=True)[:5]
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



def addcomment(request,review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                review=review,
                author=form.cleaned_data['user_name'],
                text=form.cleaned_data['text'],
                is_published=form.cleaned_data['is_published'],
                rating = form.cleaned_data['rating']
            )
            comment.save()
            rating = form.cleaned_data.get('rating')
            if rating:
                pass
            return redirect('all_reviews')
    else:
        form = AddCommentForm()

    return render(request, 'generic_form.html', {
        'form': form,
        'title': 'Добавить комментарий',
        'button_text': 'Отправить комментарий'
    })


def add_review(request):
    if request.method == 'POST':
        form = AddReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_reviews')
    else:
        form = AddReviewForm()

    return render(request, 'generic_form.html', {
        'form': form,
        'title': 'Добавить рецензию',
        'button_text': 'Опубликовать рецензию'
    })