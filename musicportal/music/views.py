from django.shortcuts import render
from music.models import Song,Album
def about_music(request):
    songs = Song.objects.all()
    albums = Album.objects.all()
    data = {
        'songs': songs,
        'albums': albums,
    }
    return render(request, 'music.html',
                  context=data)
