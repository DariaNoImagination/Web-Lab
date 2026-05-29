
from django.db.models import F, Value
from django.db.models.functions import Coalesce

class CareerLengthMixin:
    """Миксин для добавления длины карьеры в queryset"""

    def get_queryset_with_career_length(self, queryset):
        return queryset.annotate(
            career_length=Coalesce(F('active_to'), Value(2026)) - F('active_from')
        ).order_by('-career_length')


class ArtistListContextMixin:
    """Миксин для добавления общих данных в контекст списка исполнителей"""

    def get_artist_list_context(self, context, title):
        context['title'] = title
        context['years_range'] = range(1980, 2027)
        context['app_name'] = 'artists'
        return context


class ArtistDetailContextMixin:
    """Миксин для добавления данных в контекст детальной страницы исполнителя"""

    def add_career_info(self, context, artist):
        """Добавляет информацию о карьере"""
        if artist.active_from:
            end = artist.active_to if artist.active_to else 2026
            context['career_length'] = end - artist.active_from

        if artist.active_to:
            context['years_display'] = f"{artist.active_from} - {artist.active_to}"
        else:
            context['years_display'] = f"{artist.active_from} - настоящее время"
        return context

    def add_songs_and_albums(self, context, artist):
        """Добавляет песни и альбомы исполнителя"""
        from music.models import Song, Album

        context['songs'] = Song.objects.filter(artist=artist).select_related('album', 'genre')[:10]
        context['songs_count'] = context['songs'].count()
        context['albums'] = Album.objects.filter(artist=artist).select_related('genre')[:10]
        context['albums_count'] = context['albums'].count()
        return context


class TagMixin:
    """Миксин для работы с тегами"""

    def get_tag(self, tag_slug):
        from artists.models import TagPost
        from django.shortcuts import get_object_or_404
        return get_object_or_404(TagPost, slug=tag_slug)


class GenreMixin:
    """Миксин для работы с жанрами"""

    def get_genre(self, genre_slug):
        from artists.models import Genre
        from django.shortcuts import get_object_or_404
        return get_object_or_404(Genre, slug=genre_slug)