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
                'name': 'Lady Gaga',
                'genre': 'Поп',
                'favorite_songs': []
            },
        ],


        'reviews': [
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