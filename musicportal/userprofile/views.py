from django.http import HttpResponse
from django.views.generic import TemplateView
from artists.models import Artist
from music.models import Song, Album
from reviews.models import Review
from communities.models import Community
from django.views.generic.edit import UpdateView,DeleteView
from django.urls import reverse_lazy

# userprofile/views.py
class UserProfile(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем все записи из БД
        all_artists = list(Artist.objects.all())
        all_songs = list(Song.objects.select_related('artist', 'album').all())
        all_reviews = list(Review.objects.select_related('song', 'album').all())
        all_communities = list(Community.objects.all())

        # Любимые исполнители
        artists = all_artists[2], all_artists[7], all_artists[6]

        # Формируем любимых исполнителей с их песнями
        favorite_artists = []
        favorite_songs = []
        for artist in artists:
            artist_songs = [s for s in all_songs if s.artist == artist][:2]
            favorite_songs.append(artist_songs[0] if artist_songs else None)
            favorite_artists.append({
                'name': artist.title,
                'genre': artist.genre.title if artist.genre else "Не указан",
                'favorite_songs': [
                    {
                        'title': song.title,
                        'album': song.album.title if song.album else "—",
                        'year': song.year
                    } for song in artist_songs
                ]
            })


        reviews_data = []
        for review in [all_reviews[1], all_reviews[4]] if len(all_reviews) > 3 else all_reviews:
            if review.song:
                reviews_data.append({
                    'id': review.id,
                    'type': 'song',
                    'title': review.song.title,
                    'artist': review.song.artist.title if review.song.artist else "Не указан",
                    'album': review.song.album.title if review.song.album else "—",
                    'rating': review.rating,
                    'text': review.text
                })
            elif review.album:
                reviews_data.append({
                    'id': review.id,  # ← ДОБАВЬТЕ ЭТО!
                    'type': 'album',
                    'title': review.album.title,
                    'artist': review.album.artist.title if review.album.artist else "Не указан",
                    'rating': review.rating,
                    'text': review.text
                })


        context['title'] = f'Профиль: username'
        context['username'] = 'username'
        context['reviews_count'] = len(all_reviews)
        context['favorite_artists_count'] = len(artists)
        context['favorite_songs_count'] = len(favorite_songs)


        context['favorite_artists'] = favorite_artists
        context['reviews'] = reviews_data
        context['communities'] = all_communities[:1]

        return context


def edit_profile(request, username):
    return HttpResponse("<h1>Редактирование профиля</h1>")


class UpdateReview(UpdateView):
    model = Review
    fields = ['song', 'album', 'rating', 'text', 'is_published']
    template_name = 'generic_form.html'
    extra_context = {'title': 'Редактировать рецензию',
                     'button_text': 'Опубликовать рецензию'}

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})


class DeleteReview(DeleteView):
    model = Review
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = super().delete(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление рецензии'
        context['object_type'] = 'рецензию'

        if self.object.song:
            context['object_title'] = self.object.song.title
        elif self.object.album:
            context['object_title'] = self.object.album.title
        else:
            context['object_title'] = 'рецензию'

        context['cancel_url'] = self.get_success_url()
        return context