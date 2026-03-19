from django.shortcuts import render
from django.http import HttpResponse

def user_profile(request, username):
    profile_data = {
        'username': username,
        'reviews_count': 5,
        'favorite_artists_count': 4,
        'favorite_songs_count': 12,

        'favorite_artists': [
            {
                'name': 'Taylor Swift',
                'genre': 'Поп',
                'favorite_songs': [
                    {'title': 'Anti-Hero', 'album': 'Midnights', 'year': 2022},
                    {'title': 'Cruel Summer', 'album': 'Lover', 'year': 2019},
                ]
            },
            {
                'name': 'The Weeknd',
                'genre': 'R&B',
                'favorite_songs': [
                    {'title': 'Blinding Lights', 'album': 'After Hours', 'year': 2019},
                ]
            },
            {
                'name': 'Coldplay',
                'genre': 'Рок',
                'favorite_songs': [
                    {'title': 'Viva la Vida', 'album': 'Viva la Vida', 'year': 2008},
                ]
            },
            {
                'name': 'Lady Gaga',
                'genre': 'Поп',
                'favorite_songs': []
            },
        ],


        'reviews': [
            {
                'type': 'album',
                'title': 'Midnights',
                'artist': 'Taylor Swift',
                'album': 'Midnights',
                'rating': 9,
                'text': 'Отличный альбом! Очень понравились эксперименты со звуком.',
                'date': '10 марта 2025'
            },
            {
                'type': 'song',
                'title': 'Blinding Lights',
                'artist': 'The Weeknd',
                'rating': 10,
                'text': 'Одна из лучших песен последних лет!',
                'date': '5 марта 2025'
            },
        ],
        'communities': [
            {
                'name': 'Swifties',
                'description': 'Крупнейший фан-клуб Тейлор Свифт',
                'members_count': 850000,
                'join_date': '20 января 2025'
            },
            {
                'name': 'Little Monsters',
                'description': 'Сообщество Little Monsters',
                'members_count': 680000,
                'join_date': '1 февраля 2025'
            },
        ],
    }

    return render(request, 'profile.html', context=profile_data)

def edit_profile(request, username):
    return HttpResponse("<h1>Редактирование профиля<h1>")