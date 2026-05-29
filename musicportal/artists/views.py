from django.shortcuts import  redirect
from artists.models import Artist, Genre
from django.db.models import F, Q, Value
from django.urls import reverse_lazy
from django.db.models.functions import Coalesce
from .forms import AddArtistForm
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from datetime import datetime
from .utils import (
    CareerLengthMixin, ArtistListContextMixin,
    ArtistDetailContextMixin,GenreMixin,TagMixin)
from django.core.paginator import Paginator


class ArtistAll(CareerLengthMixin, ArtistListContextMixin, ListView):
    model = Artist
    template_name = 'information.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return self.get_queryset_with_career_length(Artist.objects.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context.get('page_obj')
        paginator = context.get('paginator')

        if paginator:
            context['page_range'] = paginator.page_range
        context['is_paginated'] = paginator.num_pages > 1
        return self.get_artist_list_context(context, 'Музыкальные исполнители')



class CategoriesAll(ListView):
    model = Genre
    template_name = 'categories.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Жанры'
        context['app_name'] = 'artists'
        return context


class ArtistsByGenre(CareerLengthMixin, ArtistListContextMixin, GenreMixin, ListView):
    template_name = 'information.html'
    context_object_name = 'posts'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        self.genre = self.get_genre(kwargs['genre_slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Artist.objects.filter(genre_id=self.genre)
        return self.get_queryset_with_career_length(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        page_obj = context.get('page_obj')
        paginator = context.get('paginator')


        if paginator:
            context['page_range'] = paginator.page_range
        context['is_paginated'] = paginator.num_pages > 1


        if context['posts']:
            title = f'Исполнители жанра {self.genre.title}'
        else:
            title = f'В жанре {self.genre.title} пока нет исполнителей'

        return self.get_artist_list_context(context, title)


def get_artists_word(count):
    if 11 <= count % 100 <= 19:
        return "исполнителей"
    elif count % 10 == 1:
        return "исполнитель"
    elif 2 <= count % 10 <= 4:
        return "исполнителя"
    else:
        return "исполнителей"


class TagArtistListView(CareerLengthMixin, ArtistListContextMixin, TagMixin, ListView):
    template_name = 'information.html'
    context_object_name = 'posts'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        self.tag = self.get_tag(kwargs['tag_slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.get_queryset_with_career_length(self.tag.artists.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        page_obj = context.get('page_obj')
        paginator = context.get('paginator')


        if paginator:
            context['page_range'] = paginator.page_range
        context['is_paginated'] = paginator.num_pages > 1

        artists_count = self.get_queryset().count()
        title = f'{self.tag.tag} ({artists_count} {get_artists_word(artists_count)})'

        return self.get_artist_list_context(context, title)


class ArtistsByYearsFilterView(View):
    def get(self, request):
        start_year = request.GET.get('start_year')
        end_year = request.GET.get('end_year')
        to_present = request.GET.get('to_present') == 'true'

        if not start_year:
            return redirect('all_artists')

        try:
            start_year = int(start_year)
        except (ValueError, TypeError):
            return redirect('all_artists')

        if not end_year:
            to_present = True
        else:
            try:
                end_year = int(end_year)
                if end_year == start_year:
                    to_present = True
            except (ValueError, TypeError):
                to_present = True

        if to_present:
            years_dict = {
                'start': start_year,
                'end': None,
                'is_present': True,
                'display': f'{start_year}-present'
            }
        else:
            years_dict = {
                'start': start_year,
                'end': end_year,
                'is_present': False,
                'display': f'{start_year}-{end_year}'
            }

        return redirect('year_artist', years=years_dict)


class ArtistsByYears(TemplateView):
    template_name = 'information.html'

    def dispatch(self, request, *args, **kwargs):
        self.years = kwargs['years']
        self.start = self.years['start']
        self.end = self.years['end']
        self.is_present = self.years['is_present']
        self.display = self.years['display']
        self.page_number = request.GET.get('page', 1)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_year = datetime.now().year

        artists = Artist.objects.filter(active_from__isnull=False)

        if self.is_present:
            artists = artists.filter(
                Q(active_from=self.start) & Q(active_to__isnull=True)
            )
            title = f"Исполнители, активные с {self.start} года по настоящее время"
        else:
            artists = artists.filter(
                Q(active_from=self.start) & Q(active_to=self.end)
            )
            if self.start == self.end:
                title = f"Исполнители, активные в {self.start} году"
            else:
                title = f"Исполнители, активные в период {self.start}-{self.end} годов"

        artists_data = artists.annotate(
            career_length=Coalesce(F('active_to'), Value(current_year)) - F('active_from')
        ).order_by('-career_length')


        paginator = Paginator(artists_data, 10)
        page_obj = paginator.get_page(self.page_number)


        for artist in page_obj:
            artist.is_active = artist.active_to is None
            artist.display_years = f"{artist.active_from} - {'настоящее время' if artist.is_active else artist.active_to}"
            artist.genre_title = artist.genre.title if artist.genre else "Не указан"

        context['title'] = title
        context['posts'] = page_obj
        context['start'] = self.start
        context['end'] = self.end
        context['is_present'] = self.is_present
        context['display'] = self.display
        context['total_count'] = artists_data.count()
        context['years_range'] = range(1980, current_year + 1)


        context['is_paginated'] = paginator.num_pages > 1
        context['page_obj'] = page_obj
        context['paginator'] = paginator
        context['page_range'] = paginator.page_range

        return context

class AddArtist(CreateView):
    form_class = AddArtistForm
    template_name = 'generic_form.html'
    success_url = reverse_lazy('all_artists')
    extra_context = {'title': 'Добавление исполнителя', 'button_text': 'Добавить исполнителя'}


class UpdateArtist(UpdateView):
    model = Artist
    form_class = AddArtistForm
    template_name = 'generic_form.html'
    extra_context = {'title': 'Редактировать исполнителя', 'button_text': 'Сохранить изменения'}
    success_url = reverse_lazy('all_artists')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_photo'] = self.object.photo if self.object.photo else None
        return context


class DeleteArtist(DeleteView):
    model = Artist
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('all_artists')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.photo:
            self.object.photo.delete()
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление исполнителя'
        context['object_type'] = 'исполнителя'
        context['cancel_url'] = reverse_lazy('all_artists')
        context['object_title'] = self.object.title
        return context


class ArtistDetailView(ArtistDetailContextMixin, DetailView):
    model = Artist
    template_name = 'artist_detail.html'
    context_object_name = 'artist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artist = self.object

        context = self.add_career_info(context, artist)
        context = self.add_songs_and_albums(context, artist)
        context['title'] = artist.title

        return context