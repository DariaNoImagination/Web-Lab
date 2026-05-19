from reviews.models import Review, Comment
from artists.models import Genre
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .forms import AddCommentForm,AddReviewForm
from django.views.generic import ListView,TemplateView,FormView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class ReviewsAll(ListView):
    model = Review
    template_name = 'information.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Review.published.all().order_by('-rating')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = 'Рецензии'


        for review in context['posts']:
             review.comments_list = review.comments.filter(is_published=True)[:5]
        return context


class ReviewsCategoriesView(TemplateView):
    template_name = 'categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Рецензии по жанрам'
        context['categories'] = Genre.objects.all()
        context['app_name'] = 'reviews'
        return context


class ReviewsByGenreView(TemplateView):
    template_name = 'information.html'

    def dispatch(self, request, *args, **kwargs):
        self.genre = get_object_or_404(Genre, slug=kwargs['genre_slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        reviews = Review.published.filter(
            Q(song__genre=self.genre) | Q(album__genre_id=self.genre)
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

        context['title'] = f'Рецензии жанра {self.genre.title}'
        context['posts'] = reviews

        return context


class AddComment(FormView):
    form_class = AddCommentForm
    template_name = 'generic_form.html'
    success_url = reverse_lazy('all_reviews')

    def dispatch(self, request, *args, **kwargs):
        self.review = get_object_or_404(Review, id=kwargs['review_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        comment = Comment(
            review=self.review,  # теперь review доступен
            author=form.cleaned_data['user_name'],
            text=form.cleaned_data['text'],
            is_published=form.cleaned_data['is_published'],
            created_at = timezone.now().strftime('%Y-%m-%d')
        )
        comment.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить комментарий'
        context['button_text'] = 'Отправить комментарий'
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить комментарий'
        context['button_text'] = 'Отправить комментарий'
        return context


class AddReview(CreateView):
    form_class = AddReviewForm
    template_name = 'generic_form.html'
    success_url = reverse_lazy('all_reviews')
    extra_context = { 'title': 'Добавить рецензию',
        'button_text': 'Опубликовать рецензию'}

