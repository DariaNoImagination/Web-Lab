# music/mixins.py
from django.db.models import Count
from music.models import Song, Album
from artists.models import Genre


class MusicFilterMixin:
    """Миксин для фильтрации музыки по жанру и году"""

    def filter_by_genre(self, songs, albums, genre_slug):
        if genre_slug:
            songs = songs.filter(genre__slug=genre_slug)
            albums = albums.filter(genre__slug=genre_slug)
        return songs, albums

    def filter_by_year(self, songs, albums, year):
        if year:
            try:
                year = int(year)
                songs = songs.filter(year=year)
                albums = albums.filter(year=year)
            except ValueError:
                pass
        return songs, albums

    def filter_by_content_type(self, songs, albums, content_type):
        if content_type == 'song':
            albums = Album.objects.none()
        elif content_type == 'album':
            songs = Song.objects.none()
        return songs, albums


class MusicContextMixin:
    """Миксин для добавления общих данных в контекст"""

    def get_base_context(self):
        current_year = 2026
        return {
            'genres': Genre.objects.all(),
            'years_range': range(1980, current_year + 1),
        }

    def get_new_releases(self):
        return {
            'newest_song': Song.objects.select_related('artist').order_by('-year').first(),
            'newest_album': Album.objects.select_related('artist').order_by('-year').first(),
        }

    def get_high_rated_songs(self, songs, content_type):
        if content_type == 'song':
            return None
        return songs.filter(
            review__rating__gte=8
        ).values(
            'album__title',
            'album__year'
        ).annotate(
            high_rated_count=Count('id', distinct=True)
        ).order_by('-high_rated_count')


class BaseMusicViewMixin(MusicFilterMixin, MusicContextMixin):
    """Миксин, объединяющий все музыкальные миксины"""
    pass


class CRUDContextMixin:
    """Миксин для операций удаления и редактирования с общим контекстом"""

    def get_delete_context(self, context, object_type, object_title, cancel_url):
        context['title'] = f'Удаление {object_type}'
        context['object_type'] = object_type
        context['object_title'] = object_title
        context['cancel_url'] = cancel_url
        return context

    def get_create_update_context(self, context, title, button_text):
        context['title'] = title
        context['button_text'] = button_text
        return context