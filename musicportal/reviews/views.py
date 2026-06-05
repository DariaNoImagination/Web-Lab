from reviews.models import Review,Comment
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .forms import AddCommentForm, AddReviewForm
from django.views.generic import ListView, TemplateView, FormView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .utils import BaseReviewsMixin, CRUDReviewContextMixin
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

class ReviewsAll(BaseReviewsMixin, ListView):
    model = Review
    template_name = 'information.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return self.get_published_reviews()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Рецензии'

        page_obj = context.get('page_obj')
        paginator = context.get('paginator')

        if paginator:
            context['page_range'] = paginator.page_range
        context['is_paginated'] = paginator.num_pages > 1
        reviews = context['posts']
        self.add_comments_to_reviews(reviews, limit=5)

        return context


class ReviewsCategoriesView(BaseReviewsMixin, TemplateView):
    template_name = 'categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Рецензии по жанрам'
        context['categories'] = self.get_all_genres()
        context['app_name'] = 'reviews'
        return context


class ReviewsByGenreView(BaseReviewsMixin, ListView):
    template_name = 'information.html'
    context_object_name = 'posts'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        self.genre = self.get_genre_by_slug(kwargs['genre_slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Review.published.filter(
            Q(song__genre=self.genre) | Q(album__genre_id=self.genre)
        ).select_related('song__artist', 'album__artist').order_by('-rating')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Рецензии жанра {self.genre.title}'


        reviews = context['posts']
        self.add_comments_to_reviews(reviews, limit=5)


        page_obj = context.get('page_obj')
        paginator = context.get('paginator')

        if paginator:
            context['page_range'] = paginator.page_range
        context['is_paginated'] = paginator and paginator.num_pages > 1

        return context


class AddComment(LoginRequiredMixin, CRUDReviewContextMixin, FormView):
    form_class = AddCommentForm
    template_name = 'generic_form.html'
    success_url = reverse_lazy('all_reviews')

    def dispatch(self, request, *args, **kwargs):
        self.review = get_object_or_404(Review, id=kwargs['review_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        created_at = timezone.now().strftime('%Y-%m-%d')
        comment = Comment(
            review=self.review,
            author=self.request.user,
            text=form.cleaned_data['text'],
            is_published=form.cleaned_data['is_published'],
            created_at=created_at
        )
        comment.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_comment_context(
            context,
            'Добавить комментарий',
            'Отправить комментарий'
        )



class AddReview(LoginRequiredMixin,CRUDReviewContextMixin, CreateView):
    form_class = AddReviewForm
    template_name = 'generic_form.html'
    success_url = reverse_lazy('all_reviews')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_review_context(
            context,
            'Добавить рецензию',
            'Опубликовать рецензию'
        )

    def form_valid(self, form):
        review = form.save(commit=False)
        review.author = self.request.user
        review.date = timezone.now().strftime('%Y-%m-%d')
        review.save()
        return super().form_valid(form)
