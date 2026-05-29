from reviews.models import Review
from artists.models import Genre
from django.db.models import Q
from django.shortcuts import get_object_or_404


class ReviewQueryMixin:
    """Миксин для работы с запросами рецензий"""

    def get_published_reviews(self):

        return Review.published.all().order_by('-rating')

    def get_reviews_by_genre(self, genre):

        return Review.published.filter(
            Q(song__genre=genre) | Q(album__genre_id=genre)
        ).order_by('-rating')

    def get_reviews_by_genre_values(self, genre):

        return self.get_reviews_by_genre(genre).values(
            'id',
            'rating',
            'text',
            'date',
            'song__title',
            'song__artist__title',
            'album__title',
            'album__artist_id__title'
        )


class ReviewContextMixin:
    """Миксин для добавления контекста рецензий"""

    def add_comments_to_reviews(self, reviews, limit=5):

        for review in reviews:
            review.comments_list = review.comments.filter(is_published=True)[:limit]
        return reviews

    def process_review_dict(self, review_dict):

        if review_dict['song__title']:
            review_dict['title'] = review_dict['song__title']
            review_dict['artist'] = review_dict['song__artist__title']
        else:
            review_dict['type'] = 'album'
            review_dict['title'] = review_dict['album__title']
            review_dict['artist'] = review_dict['album__artist_id__title']
        return review_dict

    def process_reviews_list(self, reviews):

        processed_reviews = []
        for review in reviews:
            processed_reviews.append(self.process_review_dict(review))
        return processed_reviews


class GenreMixin:
    """Миксин для работы с жанрами"""

    def get_genre_by_slug(self, slug):

        return get_object_or_404(Genre, slug=slug)

    def get_all_genres(self):

        return Genre.objects.all()


class CommentMixin:
    """Миксин для работы с комментариями"""

    def create_comment(self, review, author, text, is_published, created_at):
        from reviews.models import Comment
        return Comment.objects.create(
            review=review,
            author=author,
            text=text,
            is_published=is_published,
            created_at=created_at
        )


class BaseReviewsMixin(ReviewQueryMixin, ReviewContextMixin, GenreMixin, CommentMixin):
    """Базовый миксин, объединяющий все миксины рецензий"""
    pass


class CRUDReviewContextMixin:
    """Миксин для контекста CRUD операций с рецензиями"""

    def get_review_context(self, context, title, button_text):

        context['title'] = title
        context['button_text'] = button_text
        return context

    def get_comment_context(self, context, title, button_text):

        context['title'] = title
        context['button_text'] = button_text
        return context