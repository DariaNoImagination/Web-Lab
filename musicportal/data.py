all_artist_data = [
 {'id': 1, 'title': 'Taylor Swift', 'genre':'pop', 'content':
'Информация и музыка Тейлор Свифт'},
 {'id': 2, 'title': 'Billie Eilish', 'genre':'pop', 'content':
'Информация и музыка Билли Айлиш'},
{'id': 3, 'title': 'Madonna', 'genre':'pop', 'content':
'Информация и музыка Мадонны'},
{'id': 4, 'title': 'Imagine Dragons', 'genre':'rock','content':
'Информация и музыка Imagine Dragons'},
{'id': 5, 'title': 'Ariana Grande', 'genre':'pop','content':
'Информация и музыка Арианы Гранде'},
{'id': 6, 'title': 'The Weeknd', 'genre':'rnb','content':
'Информация и музыка The Weeknd'},
 {'id': 7, 'title': 'BTS', 'genre':'pop','content':
'Информация и музыка BTS'},
 {'id': 8, 'title': 'Coldplay','genre':'rock', 'content':
'Информация и музыка Coldplay'},
{'id': 9, 'title': 'Bruno Mars', 'genre':'pop','content':
'Информация и музыка Бруно Марса'},
{'id': 10, 'title': 'Lady Gaga', 'genre':'pop','content':
'Информация и музыка Леди Гаги'},
]

genres_data = [
    {'id': 1, 'title': 'Поп', 'slug': 'pop'},
    {'id': 2, 'title': 'R&B', 'slug': 'rnb'},
    {'id': 3, 'title': 'Рок', 'slug': 'rock'},
]
news_data = [
    {
        'id': 1,
        'title': 'Премия AMA пройдет 25 мая в MGM Grand Garden Arena',
        'category': 'awards',  # Концерты/мероприятия
        'content': 'Ежегодная церемония American Music Awards состоится 25 мая на легендарной арене MGM Grand Garden Arena в Лас-Вегасе. Ожидается выступление многих звезд первой величины.'
    },
    {
        'id': 2,
        'title': 'Объявлены победители Грэмми 2026',
        'category': 'awards',  # Премии
        'content': 'Стали известны имена победителей престижной музыкальной премии Грэмми 2026 года. Главные награды получили...'
    },
    {
        'id': 3,
        'title': 'BTS начнут мировой тур весной',
        'category': 'events',  # Концерты/мероприятия
        'content': 'Легендарная k-pop группа BTS анонсировала масштабный мировой тур, который стартует весной 2026 года. В рамках тура артисты посетят более 20 городов мира.'
    },
    {
        'id': 4,
        'title': 'Ариана Гранде едет в первый за семь лет тур',
        'category': 'events',  # Концерты/мероприятия
        'content': 'Ариана Гранде объявила о своем первом за последние семь лет концертном туре. Певица посетит Северную Америку и Европу с новой программой.'
    },
    {
        'id': 5,
        'title': 'Бруно Марс выпустил новый альбом',
        'category': 'new',  # Новинки
        'content': 'Долгожданный новый альбом Бруно Марса уже доступен на всех цифровых платформах. В пластинку вошло 12 треков, включая совместные работы с известными артистами.'
    },
    {
        'id': 6,
        'title': 'Тейлор Свифт выпустила новый клип',
        'category': 'new',  # Новинки
        'content': 'Тейлор Свифт порадовала поклонников новым музыкальным видео. Режиссером клипа выступила сама певица, а съемки проходили в живописных локациях.'
    },
]

songs_data = [

    {
        'id': 1,
        'artist_id': 1,
        'artist': 'Taylor Swift',
        'title': 'Shake It Off',
        'album': '1989 (Taylor\'s Version)',
        'year': 2014,
        'genre': 'pop',
    },
    {
        'id': 2,
        'artist_id': 1,
        'artist': 'Taylor Swift',
        'title': 'Anti-Hero',
        'album': 'Midnights',
        'year': 2022,
        'genre': 'pop',
    },

    {
        'id': 3,
        'artist_id': 2,
        'artist': 'Billie Eilish',
        'title': 'Therefore I Am',
        'album': 'Happier Than Ever',
        'year': 2020,
        'genre': 'pop',
    },
    {
        'id': 4,
        'artist_id': 2,
        'artist': 'Billie Eilish',
        'title': 'Bad Guy',
        'album': 'When We All Fall Asleep, Where Do We Go?',
        'year': 2019,
        'genre': 'pop',
    },


    {
        'id': 5,
        'artist_id': 3,
        'artist': 'Madonna',
        'title': 'La Isla Bonita',
        'album': 'True Blue',
        'year': 1987,
        'genre': 'pop',

    },


    {
        'id': 6,
        'artist_id': 4,
        'artist': 'Imagine Dragons',
        'title': 'Radioactive',
        'album': 'Night Visions',
        'year': 2012,
        'genre': 'rock',

    },
    {
        'id': 7,
        'artist_id': 4,
        'artist': 'Imagine Dragons',
        'title': 'Believer',
        'album': 'Evolve',
        'year': 2017,
        'genre': 'rock',
    },


    {
        'id': 8,
        'artist_id': 5,
        'artist': 'Ariana Grande',
        'title': '7 Rings',
        'album': 'Thank U, Next',
        'year': 2019,
        'genre': 'pop',
    },
    {
        'id': 9,
        'artist_id': 5,
        'artist': 'Ariana Grande',
        'title': 'We cant be friends',
        'album': 'eternal sunshine',
        'year': 2024,
        'genre': 'pop',
    },


    {
        'id': 10,
        'artist_id': 6,
        'artist': 'The Weeknd',
        'title': 'Blinding Lights',
        'album': 'After Hours',
        'year': 2019,
        'genre': 'r&b',

    },
    {
        'id': 11,
        'artist_id': 6,
        'artist': 'The Weeknd',
        'title': 'Save Your Tears',
        'album': 'Dawn FM',
        'year': 2020,
        'genre': 'r&b',

    },


    {
        'id': 12,
        'artist_id': 7,
        'artist': 'BTS',
        'title': 'Black Swan',
        'album': 'Map of the Soul: 7',
        'year': 2020,
        'genre': 'pop',
    },
    {
        'id': 13,
        'artist_id': 7,
        'artist': 'BTS',
        'title': 'Life Goes On',
        'album': 'BE',
        'year': 2020,
        'genre': 'pop',

    },


    {
        'id': 14,
        'artist_id': 8,
        'artist': 'Coldplay',
        'title': 'The Scientist',
        'album': 'A Rush of Blood to the Head',
        'year': 2002,
        'genre': 'rock',
    },
    {
        'id': 15,
        'artist_id': 8,
        'artist': 'Coldplay',
        'title': 'Viva la Vida',
        'album': 'Viva la Vida or Death and All His Friends',
        'year': 2008,
        'genre': 'rock',
    },


    {
        'id': 16,
        'artist_id': 9,
        'artist': 'Bruno Mars',
        'title': '24K Magic',
        'album': '24K Magic',
        'year': 2016,
        'genre': 'pop',
    },
    {
        'id': 17,
        'artist_id': 9,
        'artist': 'Bruno Mars',
        'title': 'Treasure',
        'album': 'Unorthodox Jukebox',
        'year': 2012,
        'genre': 'pop',
    },


    {
        'id': 18,
        'artist_id': 10,
        'artist': 'Lady Gaga',
        'title': 'Bad Romance',
        'album': 'Born This Way',
        'year': 2009,
        'genre': 'pop',
    },
    {
        'id': 19,
        'artist_id': 10,
        'artist': 'Lady Gaga',
        'title': 'Shallow',
        'album': 'A Star Is Born',
        'year': 2018,
        'genre': 'pop',
    },
]

albums_data = [
    {
        'id': 1,
        'artist_id': 1,
        'artist': 'Taylor Swift',
        'title': '1989 (Taylor\'s Version)',
        'year': 2023,
        'genre': 'pop',
        'songs_count': 16,
    },
    {
        'id': 2,
        'artist_id': 1,
        'artist': 'Taylor Swift',
        'title': 'Midnights',
        'year': 2022,
        'genre': 'pop',
        'songs_count': 13,
    },

    {
        'id': 3,
        'artist_id': 2,
        'artist': 'Billie Eilish',
        'title': 'Happier Than Ever',
        'year': 2021,
        'genre': 'pop',
        'songs_count': 16,
    },
    {
        'id': 4,
        'artist_id': 2,
        'artist': 'Billie Eilish',
        'title': 'When We All Fall Asleep, Where Do We Go?',
        'year': 2019,
        'genre': 'pop',
        'songs_count': 14,
    },
    {
        'id': 5,
        'artist_id': 3,
        'artist': 'Madonna',
        'title': 'True Blue',
        'year': 1986,
        'genre': 'pop',
        'songs_count': 9,
    },

    {
        'id': 6,
        'artist_id': 4,
        'artist': 'Imagine Dragons',
        'title': 'Night Visions',
        'year': 2012,
        'genre': 'rock',
        'songs_count': 11,
    },
    {
        'id': 7,
        'artist_id': 4,
        'artist': 'Imagine Dragons',
        'title': 'Evolve',
        'year': 2017,
        'genre': 'rock',
        'songs_count': 11,
    },

    {
        'id': 8,
        'artist_id': 5,
        'artist': 'Ariana Grande',
        'title': 'Thank U, Next',
        'year': 2019,
        'genre': 'pop',
        'songs_count': 12,
    },
    {
        'id': 9,
        'artist_id': 5,
        'artist': 'Ariana Grande',
        'title': 'eternal sunshine',
        'year': 2024,
        'genre': 'pop',
        'songs_count': 13,
    },

    {
        'id': 10,
        'artist_id': 6,
        'artist': 'The Weeknd',
        'title': 'After Hours',
        'year': 2020,
        'genre': 'R&B',
        'songs_count': 14,
    },
    {
        'id': 11,
        'artist_id': 6,
        'artist': 'The Weeknd',
        'title': 'Dawn FM',
        'year': 2022,
        'genre': 'R&B',
        'songs_count': 16,
    },


    {
        'id': 12,
        'artist_id': 7,
        'artist': 'BTS',
        'title': 'Map of the Soul: 7',
        'year': 2020,
        'genre': 'pop',
        'songs_count': 20,
    },
    {
        'id': 13,
        'artist_id': 7,
        'artist': 'BTS',
        'title': 'BE',
        'year': 2020,
        'genre': 'pop',
        'songs_count': 8,
    },

    {
        'id': 14,
        'artist_id': 8,
        'artist': 'Coldplay',
        'title': 'A Rush of Blood to the Head',
        'year': 2002,
        'genre': 'rock',
        'songs_count': 11,
    },
    {
        'id': 15,
        'artist_id': 8,
        'artist': 'Coldplay',
        'title': 'Viva la Vida or Death and All His Friends',
        'year': 2008,
        'genre': 'rock',
        'songs_count': 10,
    },
    {
        'id': 16,
        'artist_id': 9,
        'artist': 'Bruno Mars',
        'title': '24K Magic',
        'year': 2016,
        'genre': 'pop',
        'songs_count': 9,
    },
    {
        'id': 17,
        'artist_id': 9,
        'artist': 'Bruno Mars',
        'title': 'Unorthodox Jukebox',
        'year': 2012,
        'genre': 'pop',
        'songs_count': 10,
    },

    # Lady Gaga
    {
        'id': 18,
        'artist_id': 10,
        'artist': 'Lady Gaga',
        'title': 'The Fame',
        'year': 2008,
        'genre': 'pop',
        'songs_count': 14,
    },
    {
        'id': 19,
        'artist_id': 10,
        'artist': 'Lady Gaga',
        'title': 'A Star Is Born',
        'year': 2018,
        'genre': 'pop',
        'songs_count': 34,
    },
]
reviews_data = [
    {
        'type': 'album',
        'title': 'Midnights',
        'artist': 'Taylor Swift',
        'rating': 9,
        'text': 'Отличный альбом! Очень понравились эксперименты со звуком.',
        'date': '10 марта 2025',
        'genre': 'pop'
    },
    {
        'type': 'song',
        'title': 'Blinding Lights',
        'artist': 'The Weeknd',
        'rating': 10,
        'text': 'Одна из лучших песен последних лет!',
        'date': '5 марта 2025',
        'genre': 'rnb'
    },
]

