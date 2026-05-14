from django.shortcuts import render,redirect
from music.models import Song, Album
from django.db.models import Count, Q
from artists.models import Genre
from .forms import AddSongForm,AddAlbumForm

def filter_music(request):


    genre_slug = request.GET.get('genre')
    content_type = request.GET.get('content_type')
    year = request.GET.get('year')

    songs = Song.objects.select_related('artist', 'genre', 'album')
    albums = Album.objects.select_related('artist', 'genre')

    if genre_slug:
        songs = songs.filter(genre__slug=genre_slug)
        albums = albums.filter(genre__slug=genre_slug)

    if year:
        try:
            year = int(year)
            songs = songs.filter(year=year)
            albums = albums.filter(year=year)
        except ValueError:
            pass


    high_rated_songs_by_album = None
    if content_type != 'song':
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


    if content_type == 'song':
        albums = Album.objects.none()
    elif content_type == 'album':
        songs = Song.objects.none()

    genres = Genre.objects.all()
    current_year = 2026
    years_range = range(1980, current_year + 1)

    context = {
        'songs': songs,
        'albums': albums,
        'newest_song': new_song,
        'newest_album': new_album,
        'high_rated_songs_by_album': high_rated_songs_by_album,
        'genres': genres,
        'years_range': years_range,
        'selected_genre': genre_slug,
        'selected_type': content_type,
        'selected_year': year,
    }
    return render(request, 'music.html', context)


def about_music(request):
    songs = Song.objects.select_related('artist', 'genre', 'album').all()
    albums = Album.objects.select_related('artist', 'genre').all()
    current_year = 2026
    years_range = range(1980, current_year + 1)
    new_song = Song.objects.order_by("-year").first()
    new_album = Album.objects.latest("year")
    genres = Genre.objects.all()
    data = {
        'years_range': years_range,
        'songs': songs,
        'albums': albums,
        'genres': genres,
        'newest_song': new_song,
        'newest_album': new_album
    }
    return render(request, 'music.html', context=data)


def add_album(request):
    if request.method == 'POST':
        form = AddAlbumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_music')
    else:
        form = AddAlbumForm()

    return render(request, 'generic_form.html', {
        'form': form,
        'title': 'Добавить альбом',
        'button_text': 'Добавить альбом'
    })


def add_song(request):
    if request.method == 'POST':
        form = AddSongForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_music')
    else:
        form = AddSongForm()

    return render(request, 'generic_form.html', {
        'form': form,
        'title': 'Добавить песню',
        'button_text': 'Добавить песню'
    })