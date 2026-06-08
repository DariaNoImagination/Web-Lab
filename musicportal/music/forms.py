from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from .models import Album, Song

class AddAlbumForm(forms.ModelForm):
    year = forms.IntegerField(
        min_value=1900,
        max_value=2026,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'например: 2020'}),
        label='Год выпуска',
        help_text='Введите год выпуска альбома (от 1900 до 2026)',
        validators=[
            MinValueValidator(1900, message="Год не может быть раньше 1900"),
            MaxValueValidator(2026, message="Год не может быть позже 2026")
        ]
    )

    songs_count = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'например: 12'}),
        label='Количество песен',
        help_text='Введите количество песен в альбоме (опционально)',
        validators=[
            MinValueValidator(1, message="Количество песен не может быть меньше 1"),
            MaxValueValidator(100, message="Количество песен не может превышать 100")
        ]
    )

    class Meta:
        model = Album
        fields = ['title', 'artist', 'year', 'genre', 'songs_count']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите название альбома'
            }),
            'artist': forms.Select(attrs={'class': 'form-select'}),
            'genre': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'title': 'Название альбома',
            'artist': 'Исполнитель',
            'year': 'Год выпуска',
            'genre': 'Жанр',
            'songs_count': 'Количество песен',
        }
        help_texts = {
            'title': 'Введите официальное название альбома',
            'artist': 'Выберите исполнителя',
            'genre': 'Выберите жанр альбома',
        }
        error_messages = {
            'title': {
                'required': 'Пожалуйста, введите название альбома',
                'max_length': 'Название не должно превышать 255 символов',
            },
            'artist': {
                'required': 'Выберите исполнителя',
            },
            'genre': {
                'required': 'Выберите жанр',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['artist'].empty_label = 'Выберите исполнителя'
        self.fields['genre'].empty_label = 'Выберите жанр'


        self.fields['title'].validators.append(
            MinLengthValidator(2, message="Минимум 2 символа")
        )

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            title = ' '.join(title.split())
            # Проверка на дубликаты
            if Album.objects.filter(title__iexact=title).exists():
                if not self.instance.pk or self.instance.title != title:
                    raise forms.ValidationError('Альбом с таким названием уже существует')
        return title



class AddSongForm(forms.ModelForm):
    year = forms.IntegerField(
        min_value=1900,
        max_value=2026,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'например: 2020'}),
        label='Год выпуска',
        help_text='Введите год выпуска песни (от 1900 до 2026)',
        validators=[
            MinValueValidator(1900, message="Год не может быть раньше 1900"),
            MaxValueValidator(2026, message="Год не может быть позже 2026")
        ]
    )

    class Meta:
        model = Song
        fields = ['title', 'artist', 'album', 'year', 'genre']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите название песни'
            }),
            'artist': forms.Select(attrs={'class': 'form-select'}),
            'album': forms.Select(attrs={'class': 'form-select'}),
            'genre': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'title': 'Название песни',
            'artist': 'Исполнитель',
            'album': 'Альбом',
            'year': 'Год выпуска',
            'genre': 'Жанр',
        }
        help_texts = {
            'title': 'Введите название песни',
            'artist': 'Выберите исполнителя',
            'album': 'Выберите альбом (если есть)',
            'genre': 'Выберите жанр песни',
        }
        error_messages = {
            'title': {
                'required': 'Пожалуйста, введите название песни',
                'max_length': 'Название не должно превышать 255 символов',
            },
            'artist': {
                'required': 'Выберите исполнителя',
            },
            'genre': {
                'required': 'Выберите жанр',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['artist'].empty_label = 'Выберите исполнителя'
        self.fields['album'].empty_label = 'Выберите альбом (необязательно)'
        self.fields['genre'].empty_label = 'Выберите жанр'
        self.fields['album'].required = False




        self.fields['title'].validators.append(
            MinLengthValidator(2, message="Минимум 2 символа")
        )


        if 'artist' in self.data:
            try:
                artist_id = int(self.data.get('artist'))
                self.fields['album'].queryset = Album.objects.filter(artist_id=artist_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.artist:
            self.fields['album'].queryset = Album.objects.filter(artist=self.instance.artist)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            title = ' '.join(title.split())
        return title

    def clean(self):
        cleaned_data = super().clean()
        artist = cleaned_data.get('artist')
        album = cleaned_data.get('album')


        if artist and album and album.artist != artist:
            raise forms.ValidationError('Выбранный альбом не принадлежит указанному исполнителю')

        return cleaned_data

