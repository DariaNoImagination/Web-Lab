from reviews.models import Review
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .forms import AddCommentForm, AddReviewForm
from django.views.generic import ListView, TemplateView, FormView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .utils import BaseReviewsMixin, CRUDReviewContextMixin


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
        context['is_paginated'] = True
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


class ReviewsByGenreView(BaseReviewsMixin, TemplateView):
    template_name = 'information.html'
    paginate_by = 10
    def dispatch(self, request, *args, **kwargs):
        self.genre = self.get_genre_by_slug(kwargs['genre_slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        reviews = self.get_reviews_by_genre_values(self.genre)
        processed_reviews = self.process_reviews_list(reviews)

        context['title'] = f'Рецензии жанра {self.genre.title}'
        context['posts'] = processed_reviews
        page_obj = context.get('page_obj')
        paginator = context.get('paginator')

        if paginator:
            context['page_range'] = paginator.page_range
        context['is_paginated'] = True

        return context


class AddComment(BaseReviewsMixin, CRUDReviewContextMixin, FormView):
    form_class = AddCommentForm
    template_name = 'generic_form.html'
    success_url = reverse_lazy('all_reviews')

    def dispatch(self, request, *args, **kwargs):
        self.review = get_object_or_404(Review, id=kwargs['review_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        created_at = timezone.now().strftime('%Y-%m-%d')

        self.create_comment(
            review=self.review,
            author=form.cleaned_data['user_name'],
            text=form.cleaned_data['text'],
            is_published=form.cleaned_data['is_published'],
            created_at=created_at
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_comment_context(
            context,
            'Добавить комментарий',
            'Отправить комментарий'
        )


class AddReview(CRUDReviewContextMixin, CreateView):
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