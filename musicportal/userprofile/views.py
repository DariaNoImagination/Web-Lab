from django.views import View
from reviews.models import Review
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileUserForm
from communities.models import Community
from artists.models import Artist
from music.models import Song,Album
from django.shortcuts import  redirect
from django.http import JsonResponse
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'profile.html'
    extra_context = {'title': 'Профиль пользователя'}

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('userprofile:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['username'] = user.username

        # Любимые исполнители
        if hasattr(user, 'favorite_artists'):
            favorite_artists = user.favorite_artists.all()
            context['favorite_artists'] = favorite_artists
            context['favorite_artists_count'] = favorite_artists.count()
        else:
            context['favorite_artists'] = []
            context['favorite_artists_count'] = 0

        # Любимые песни
        if hasattr(user, 'favorite_songs'):
            favorite_songs = user.favorite_songs.all()
            context['favorite_songs'] = favorite_songs
            context['favorite_songs_count'] = favorite_songs.count()
        else:
            context['favorite_songs'] = []
            context['favorite_songs_count'] = 0

        # Любимые альбомы
        if hasattr(user, 'favorite_albums'):
            favorite_albums = user.favorite_albums.all()
            context['favorite_albums'] = favorite_albums
            context['favorite_albums_count'] = favorite_albums.count()
        else:
            context['favorite_albums'] = []
            context['favorite_albums_count'] = 0

        user_reviews = []
        # Рецензии
        all_reviews = Review.objects.all()
        for review in all_reviews:
            if review.author == user:
                user_reviews.append(review)


        context['reviews'] = user_reviews
        context['reviews_count'] = len(user_reviews)


        # Сообщества
        if hasattr(user, 'joined_communities'):
            communities = user.joined_communities.all()
            context['communities'] = communities
        else:
            context['communities'] = []

        return context

    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.FILES.get('avatar'):
            user = self.get_object()
            user.avatar = request.FILES['avatar']
            user.save()
            return JsonResponse({
                'success': True,
                'avatar_url': user.avatar.url
            })


        return super().post(request, *args, **kwargs)


class BaseToggleFavoriteView(LoginRequiredMixin, View):
    model = None
    favorite_field = None
    success_url_name = None

    def get_object(self, obj_id):
        return get_object_or_404(self.model, id=obj_id)

    def is_favorite(self, user, obj):
        return getattr(user, self.favorite_field).filter(id=obj.id).exists()

    def add_favorite(self, user, obj):
        getattr(user, self.favorite_field).add(obj)

    def remove_favorite(self, user, obj):
        getattr(user, self.favorite_field).remove(obj)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', reverse_lazy(self.success_url_name))

    def post(self, request, *args, **kwargs):
        obj_id = kwargs.get('pk')
        obj = self.get_object(obj_id)

        if self.is_favorite(request.user, obj):
            self.remove_favorite(request.user, obj)
            status = 'removed'
        else:
            self.add_favorite(request.user, obj)
            status = 'added'

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': status,
                'message': f'{"Добавлено" if status == "added" else "Удалено"} в избранное'
            })


        return redirect(request.META.get('HTTP_REFERER', reverse_lazy(self.success_url_name)))



class ToggleFavoriteArtistView(BaseToggleFavoriteView):
    model = Artist
    favorite_field = 'favorite_artists'
    success_url_name = 'all_artists'


class FavoriteArtistsListView(LoginRequiredMixin, ListView):
    template_name = 'favorites/artists.html'
    context_object_name = 'artists'

    def get_queryset(self):
        return self.request.user.favorite_artists.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Любимые исполнители'
        return context



class ToggleFavoriteSongView(BaseToggleFavoriteView):
    model = Song
    favorite_field = 'favorite_songs'
    success_url_name = 'all_music'


class FavoriteSongsListView(LoginRequiredMixin, ListView):
    template_name = 'favorites/songs.html'
    context_object_name = 'songs'

    def get_queryset(self):
        return self.request.user.favorite_songs.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Любимые песни'
        return context


class ToggleFavoriteAlbumView(BaseToggleFavoriteView):
    model = Album
    favorite_field = 'favorite_albums'
    success_url_name = 'all_music'


class FavoriteAlbumsListView(LoginRequiredMixin, ListView):
    template_name = 'favorites/albums.html'
    context_object_name = 'albums'

    def get_queryset(self):
        return self.request.user.favorite_albums.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Любимые альбомы'
        return context



class ToggleCommunityView(BaseToggleFavoriteView):
    model = Community
    favorite_field = 'joined_communities'
    success_url_name = 'all_communities'

    def add_favorite(self, user, obj):
        getattr(user, self.favorite_field).add(obj)
        obj.members += 1
        obj.save()

    def remove_favorite(self, user, obj):
        getattr(user, self.favorite_field).remove(obj)
        if obj.members > 0:
            obj.members -= 1
            obj.save()

    def is_favorite(self, user, obj):
        return getattr(user, self.favorite_field).filter(id=obj.id).exists()

    def post(self, request, *args, **kwargs):
        obj_id = kwargs.get('pk')
        obj = self.get_object(obj_id)

        if self.is_favorite(request.user, obj):
            self.remove_favorite(request.user, obj)
            status = 'removed'
        else:
            self.add_favorite(request.user, obj)
            status = 'added'

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': status,
                'members_count': obj.members,
            })


class JoinedCommunitiesListView(LoginRequiredMixin, ListView):
    template_name = 'favorites/communities.html'
    context_object_name = 'communities'

    def get_queryset(self):
        return self.request.user.joined_communities.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мои сообщества'
        return context

