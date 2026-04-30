from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Album, Song




@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_artist', 'year', 'get_genre', 'songs_count')
    list_filter = ('year', 'genre', 'artist')
    search_fields = ('title', 'artist__title')

    def get_artist(self, obj):
        return obj.artist.title if obj.artist else "—"

    get_artist.short_description = 'Исполнитель'

    def get_genre(self, obj):
        return obj.genre.title if obj.genre else "—"

    get_genre.short_description = 'Жанр'


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_artist', 'album', 'year', 'get_genre')
    list_filter = ('year', 'genre', 'artist')
    search_fields = ('title', 'artist__title')

    def get_artist(self, obj):
        return obj.artist.title if obj.artist else "—"

    get_artist.short_description = 'Исполнитель'

    def get_genre(self, obj):
        return obj.genre.title if obj.genre else "—"

    get_genre.short_description = 'Жанр'
