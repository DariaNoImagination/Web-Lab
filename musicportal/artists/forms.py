from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .models import Artist


class AddArtistForm(forms.ModelForm):
    active_from = forms.IntegerField(
        required=False,
        min_value=1900,
        max_value=2026,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'например: 2000'}),
        label='Активен с',
        help_text='Год начала карьеры (от 1900 до 2026)'
    )

    active_to = forms.IntegerField(
        required=False,
        min_value=1900,
        max_value=2026,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'например: 2020'}),
        label='Активен по',
        help_text='Год окончания карьеры (если активен - оставьте пустым)'
    )

    class Meta:
        model = Artist
        fields = ['title', 'genre', 'content', 'tags', 'active_from', 'active_to', 'photo']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите имя исполнителя'}),
            'genre': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'form-textarea',
                                             'placeholder': 'Расскажите об исполнителе...'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
        labels = {
            'title': 'Имя исполнителя',
            'genre': 'Жанр',
            'content': 'Описание',
            'tags': 'Теги',
            'active_from': 'Активен с',
            'active_to': 'Активен по',
        }
        help_texts = {
            'title': 'Введите полное имя исполнителя или группы',
            'genre': 'Выберите основной жанр музыки',
            'content': 'Краткая биография и творческий путь',
            'tags': 'Выберите теги для категоризации (можно несколько) при нажатии на Ctrl',
        }
        error_messages = {
            'title': {
                'required': 'Пожалуйста, введите имя исполнителя',
                'max_length': 'Имя не должно превышать 255 символов',
            },
            'genre': {
                'required': 'Выберите жанр исполнителя',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['genre'].empty_label = 'Выберите жанр'
        self.fields['tags'].required = False


        # Добавляем валидаторы для текста
        self.fields['content'].validators.append(MinLengthValidator(10, message="Минимум 10 символов"))
        self.fields['content'].validators.append(MaxLengthValidator(5000, message="Максимум 5000 символов"))

        # Добавляем валидаторы для имени
        self.fields['title'].validators.append(MinLengthValidator(2, message="Минимум 2 символа"))
        self.fields['title'].validators.append(MaxLengthValidator(255, message="Максимум 255 символов"))

    def clean(self):
        cleaned_data = super().clean()
        active_from = cleaned_data.get('active_from')
        active_to = cleaned_data.get('active_to')


        if active_from and active_to and active_to < active_from:
            raise forms.ValidationError('Год окончания карьеры не может быть раньше года начала')


        if active_from and active_from > 2026:
            raise forms.ValidationError('Год начала не может быть в будущем')


        if active_to and active_to < 1900:
            raise forms.ValidationError('Год окончания не может быть раньше 1900')

        return cleaned_data

    def clean_title(self):

        title = self.cleaned_data.get('title')
        if title:

            if Artist.objects.filter(title__iexact=title).exists():
                if not self.instance.pk or self.instance.title != title:
                    raise forms.ValidationError('Исполнитель с таким именем уже существует')
            title = ' '.join(title.split())
        return title

