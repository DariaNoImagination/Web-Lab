from django.shortcuts import render, get_object_or_404,redirect
from artists.models import Artist,Genre,TagPost
from django.db.models import F,Q,Value
from django.urls import reverse_lazy
from django.db.models.functions import Coalesce
from .forms import  AddArtistForm
from django.views.generic import ListView,TemplateView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from datetime import datetime
from django.contrib import messages


class ArtistAll(ListView):
    model = Artist
    template_name = 'information.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Artist.objects.annotate(
            career_length=Coalesce(F('active_to'), Value(2026)) - F('active_from')
        ).order_by('-career_length')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Музыкальные исполнители'
        context['years_range'] = range(1980, 2027)
        return context

class CategoriesAll(ListView):
    model = Genre
    template_name = 'categories.html'
    context_object_name = 'categories'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Жанры'
        context['app_name'] = 'artists'
        return context

class ArtistsByGenre(ListView):
    template_name = 'information.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.genre = get_object_or_404(Genre, slug=self.kwargs['genre_slug'])

        return Artist.objects.filter(genre_id=self.genre).annotate(
            career_length=Coalesce(F('active_to'), Value(2026)) - F('active_from')
        ).order_by('-career_length')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if context['posts']:
            context['title'] = f'Исполнители жанра {self.genre.title}'
        else:
            context['title'] = f'В жанре {self.genre.title} пока нет исполнителей'

        context['years_range'] = range(1980, 2027)
        context['app_name'] = 'artists'

        return context


def get_artists_word(count):
    if 11 <= count % 100 <= 19:
        return "исполнителей"
    elif count % 10 == 1:
        return "исполнитель"
    elif 2 <= count % 10 <= 4:
        return "исполнителя"
    else:
        return "исполнителей"

def show_tag_artistlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    artists = tag.artists
    artists_data = artists.annotate(
        career_length=Coalesce(F('active_to'), Value(2026)) - F('active_from')
    ).order_by('-career_length')
    artists_count = artists.count()
    data = {
        'title': f'{tag.tag} ({artists_count} {get_artists_word(artists_count)})',
        'posts': artists_data,
        'app_name': 'artists'
     }
    return render(request, 'information.html', context=data)


def artists_by_years_filter(request):
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


        for artist in artists_data:
            artist.is_active = artist.active_to is None
            artist.display_years = f"{artist.active_from} - {'настоящее время' if artist.is_active else artist.active_to}"
            artist.genre_title = artist.genre.title if artist.genre else "Не указан"

        context['title'] = title
        context['posts'] = artists_data
        context['start'] = self.start
        context['end'] = self.end
        context['is_present'] = self.is_present
        context['display'] = self.display
        context['total_count'] = artists_data.count()
        context['years_range'] = range(1980, current_year + 1)

        return context

class AddArtist(CreateView):
    form_class = AddArtistForm
    template_name = 'generic_form.html'
    success_url = reverse_lazy('all_artists')
    extra_context = {'title': 'Добавление исполнителя','button_text': 'Добавить исполнителя'}


class UpdateArtist(UpdateView):
    model = Artist
    form_class = AddArtistForm
    template_name = 'generic_form.html'
    extra_context = {'title': 'Редактировать исполнителя',
                     'button_text': 'Сохранить изменения'}
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
        messages.success(request, f'Исполнитель "{self.object.title}" успешно удалён')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление исполнителя'
        context['object_type'] = 'исполнителя'
        context['cancel_url'] = reverse_lazy('all_artists')
        context['object_title'] = self.object.title
        return context


