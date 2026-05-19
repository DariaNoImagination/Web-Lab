from music.models import Song, Album
from django.db.models import Count
from artists.models import Genre
from .forms import AddSongForm,AddAlbumForm
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy

class FilterMusicView(TemplateView):
    template_name = 'music.html'

    def get(self, request, *args, **kwargs):
        self.genre_slug = request.GET.get('genre')
        self.content_type = request.GET.get('content_type')
        self.year = request.GET.get('year')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        songs = Song.objects.select_related('artist', 'genre', 'album')
        albums = Album.objects.select_related('artist', 'genre')

        if self.genre_slug:
            songs = songs.filter(genre__slug=self.genre_slug)
            albums = albums.filter(genre__slug=self.genre_slug)

        year = self.year
        if year:
            try:
                year = int(year)
                songs = songs.filter(year=year)
                albums = albums.filter(year=year)
            except ValueError:
                pass

        high_rated_songs_by_album = None
        if self.content_type != 'song':
            high_rated_songs_by_album = songs.filter(
                review__rating__gte=8
            ).values(
                'album__title',
                'album__year'
            ).annotate(
                high_rated_count=Count('id', distinct=True)
            ).order_by('-high_rated_count')

        new_song = Song.objects.select_related('artist').order_by('-year').first()
        new_album = Album.objects.select_related('artist').order_by('-year').first()

        if self.content_type == 'song':
            albums = Album.objects.none()
        elif self.content_type == 'album':
            songs = Song.objects.none()

        genres = Genre.objects.all()
        current_year = 2026
        years_range = range(1980, current_year + 1)

        context['songs'] = songs
        context['albums'] = albums
        context['newest_song'] = new_song
        context['newest_album'] = new_album
        context['high_rated_songs_by_album'] = high_rated_songs_by_album
        context['genres'] = genres
        context['years_range'] = years_range
        context['selected_genre'] = self.genre_slug
        context['selected_type'] = self.content_type
        context['selected_year'] = self.year
        return context


class AboutMusic(TemplateView):
    template_name = 'music.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        songs = Song.objects.select_related('artist', 'genre', 'album').all()
        albums = Album.objects.select_related('artist', 'genre').all()
        current_year = 2026
        years_range = range(1980, current_year + 1)
        new_song = Song.objects.order_by("-year").first()
        new_album = Album.objects.latest("year")
        genres = Genre.objects.all()

        context['songs'] = songs
        context['albums'] = albums
        context['years_range'] = years_range
        context['genres'] = genres
        context['newest_song'] = new_song
        context['newest_album'] = new_album
        context['title'] = 'Каталог музыки'

        return context

class AddAlbum(CreateView):
    form_class = AddAlbumForm
    template_name = 'generic_form.html'
    success_url = reverse_lazy('all_music')
    extra_context = {'title': 'Добавить альбом',
        'button_text': 'Добавить альбом'}

class AddSong(CreateView):
    form_class = AddSongForm
    template_name = 'generic_form.html'
    success_url = reverse_lazy('all_music')
    extra_context = {'title': 'Добавить песню',
        'button_text': 'Добавить песню'}

class UpdateAlbum(UpdateView):
    model = Album
    form_class = AddAlbumForm
    template_name = 'generic_form.html'
    success_url = reverse_lazy('all_music')
    extra_context = {'title': 'Редактировать альбом',
        'button_text': 'Сохранить изменения'}

class UpdateSong(UpdateView):
    model = Song
    form_class = AddSongForm
    template_name = 'generic_form.html'
    success_url = reverse_lazy('all_music')
    extra_context = {'title': 'Редактировать песню',
        'button_text': 'Сохранить изменения'}

class DeleteAlbum(DeleteView):
    model = Album
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('all_music')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = super().delete(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление альбома'
        context['object_type'] = 'альбом'
        context['object_title'] = self.object.title
        context['cancel_url'] = reverse_lazy('all_music')
        return context


class DeleteSong(DeleteView):
    model = Song
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('all_music')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = super().delete(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление песни'
        context['object_type'] = 'песню'
        context['object_title'] = self.object.title
        context['cancel_url'] = reverse_lazy('all_music')
        return context