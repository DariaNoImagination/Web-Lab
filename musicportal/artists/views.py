from django.shortcuts import render, get_object_or_404,redirect
from artists.models import Artist,Genre,TagPost
from django.db.models import F,Q,Value
from django.db.models.functions import Coalesce
from django.urls import register_converter
from .converters import  YearRangeConverter

register_converter(YearRangeConverter, 'year_range')

def index(request):
    artists  = Artist.objects.all()
    artists_data = artists.annotate(
        career_length=Coalesce(F('active_to'), Value(2026)) - F('active_from')
    ).values(
        'id', 'title', 'active_from', 'active_to','genre_id__title','content',
    ).order_by('-career_length')
    data = {
        'title': 'Музыкальные исполнители',
        'years_range': range(1980, 2027),
        'posts': artists_data,
    }
    return render(request, 'information.html',
                  context=data)


def categories(request):  # Жанры
    genres = Genre.objects.all()
    data = {
        'title': 'Жанры',
        'categories': genres,
        'app_name': 'artists'
    }
    return render(request, 'categories.html', context=data)


def artists_by_genre(request, genre_slug):
    genre = get_object_or_404(Genre, slug=genre_slug)

    if not Artist.objects.filter(genre_id=genre).exists():
        data = {
            'title': f'В жанре {genre.title} пока нет исполнителей',
            'posts': [],
            'app_name': 'artists'
        }
        return render(request, 'information.html', context=data)
    artists = Artist.objects.filter(genre_id=genre)
    artists_data = artists.annotate(
        career_length=Coalesce(F('active_to'), Value(2026)) - F('active_from')
    ).values(
        'id', 'title', 'active_from', 'active_to', 'genre_id__title', 'content',
    ).order_by('-career_length')
    data = {
        'title': f'Исполнители жанра {genre.title}',
        'posts': artists_data,
        'app_name': 'artists'
    }
    return render(request, 'information.html', context=data)


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
    artists = tag.artists.values('id', 'title', 'active_from', 'active_to', 'genre_id__title', 'content')
    artists_data = artists.annotate(
        career_length=Coalesce(F('active_to'), Value(2026)) - F('active_from')
    ).values(
        'id', 'title', 'active_from', 'active_to', 'genre_id__title', 'content',
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


def artists_by_years(request, years):
    start = years['start']
    end = years['end']
    is_present = years['is_present']
    display = years['display']

    artists = Artist.objects.filter(active_from__isnull=False)

    if is_present:

        artists = artists.filter(
            Q(active_from=start) &
            Q(active_to__isnull=True)
        )
        title = f"Исполнители, активные с {start} года по настоящее время"
    else:

        artists = artists.filter(
            Q(active_from=start) &
            Q(active_to=end)
        )

        if start == end:
            title = f"Исполнители, активные в {start} году"
        else:
            title = f"Исполнители, активные в период {start}-{end} годов"


    from datetime import datetime
    current_year = datetime.now().year


    artists_data = artists.annotate(
        career_length=Coalesce(F('active_to'), Value(current_year)) - F('active_from')
    ).values(
        'id', 'title', 'active_from', 'active_to', 'career_length', 'genre__title', 'content'
    ).order_by('-career_length')


    for artist in artists_data:
        artist['is_active'] = artist['active_to'] is None
        artist[
            'display_years'] = f"{artist['active_from']} - {'настоящее время' if artist['is_active'] else artist['active_to']}"
        artist['genre_title'] = artist['genre__title']

    context = {
        'title': title,
        'posts': artists_data,
        'start': start,
        'end': end,
        'is_present': is_present,
        'display': display,
        'total_count': len(artists_data),
        'years_range': range(1980, current_year + 1),
    }
    return render(request, 'information.html', context)