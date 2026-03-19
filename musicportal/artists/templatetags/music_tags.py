from django import template

all_artist_data = [
    {'id': 1, 'title': 'Taylor Swift', 'genre': 'pop', 'content': 'Информация и музыка Тейлор Свифт'},
    {'id': 2, 'title': 'Billie Eilish', 'genre': 'pop', 'content': 'Информация и музыка Билли Айлиш'},
    {'id': 3, 'title': 'Madonna', 'genre': 'pop', 'content': 'Информация и музыка Мадонны'},
    {'id': 4, 'title': 'Imagine Dragons', 'genre': 'rock', 'content': 'Информация и музыка Imagine Dragons'},
    {'id': 5, 'title': 'Ariana Grande', 'genre': 'pop', 'content': 'Информация и музыка Арианы Гранде'},
    {'id': 6, 'title': 'The Weeknd', 'genre': 'rnb', 'content': 'Информация и музыка The Weeknd'},
    {'id': 7, 'title': 'BTS', 'genre': 'pop', 'content': 'Информация и музыка BTS'},
    {'id': 8, 'title': 'Coldplay', 'genre': 'rock', 'content': 'Информация и музыка Coldplay'},
    {'id': 9, 'title': 'Bruno Mars', 'genre': 'pop', 'content': 'Информация и музыка Бруно Марса'},
    {'id': 10, 'title': 'Lady Gaga', 'genre': 'pop', 'content': 'Информация и музыка Леди Гаги'},
]

communities_data = [
    {
        'artist_id': 1,
        'artist_name': 'Taylor Swift',
        'club_name': 'Swifties',
        'founded': '2006-10-24',
        'members': 850000,
        'description': 'Крупнейший фан-клуб Тейлор Свифт'
    },

    {
        'artist_id': 3,
        'artist_name': 'Madonna',
        'club_name': 'Madonna Fans',
        'founded': '1983-04-15',
        'members': 310000,
        'description': 'Фан-клуб королевы поп-музыки'
    },
    {
        'artist_id': 4,
        'artist_name': 'Imagine Dragons',
        'club_name': 'Dragons Family',
        'founded': '2012-09-04',
        'members': 280000,
        'description': 'Сообщество фанатов Imagine Dragons'
    },
    {
        'artist_id': 5,
        'artist_name': 'Ariana Grande',
        'club_name': 'Arianators',
        'founded': '2013-03-25',
        'members': 560000,
        'description': 'Фан-клуб Арианы Гранде'
    },
    {
        'artist_id': 7,
        'artist_name': 'BTS',
        'club_name': 'ARMY',
        'founded': '2013-06-13',
        'members': 1200000,
        'description': 'Международный фан-клуб BTS'
    },
    {
        'artist_id': 8,
        'artist_name': 'Coldplay',
        'club_name': 'Coldplayers',
        'founded': '2000-07-10',
        'members': 450000,
        'description': 'Фан-клуб Coldplay'
    },
    {
        'artist_id': 9,
        'artist_name': 'Bruno Mars',
        'club_name': 'Hooligans',
        'founded': '2010-10-04',
        'members': 320000,
        'description': 'Фан-клуб Бруно Марса'
    },
    {
        'artist_id': 10,
        'artist_name': 'Lady Gaga',
        'club_name': 'Little Monsters',
        'founded': '2008-08-19',
        'members': 680000,
        'description': 'Сообщество Little Monsters'
    }
]

register = template.Library()

@register.simple_tag()
def get_artists_info():
    return all_artist_data

@register.inclusion_tag('list_communities.html')
def show_categories():
    communities = communities_data
    return {"communities": communities}