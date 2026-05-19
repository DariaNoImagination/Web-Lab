from django import forms
from django.core.validators import MinLengthValidator,MaxLengthValidator,ValidationError
from  .models import Review
from  music.models import Song,Album
class ProfanityValidator:

    def __init__(self, bad_words_list=None):
        self.bad_words = bad_words_list or ['запрещенное слово', 'плохое слово']

    def __call__(self, value):
        value_lower = value.lower()
        for word in self.bad_words:
            if word.lower() in value_lower:
                raise ValidationError(f"Комментарий содержит запрещённое слово: {word}")

class NoSpamValidator:

    def __init__(self, min_words=3):
        self.min_words = min_words

    def __call__(self, value):
        words = value.split()
        if len(words) < self.min_words:
            raise ValidationError(
                f"Комментарий должен содержать минимум {self.min_words} слова"
            )

class AddCommentForm(forms.Form):
    user_name = forms.CharField(max_length=100, label="Имя")
    text = forms.CharField(widget=forms.Textarea, label="Комментарий",validators=[ProfanityValidator(),NoSpamValidator(), MinLengthValidator(5, message="Минимум 5 символов"), MaxLengthValidator(100, message="Максимум 100 символов"),
 ])
    is_published = forms.BooleanField(required=False, initial=True, label="Статус")


class AddReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, f'{i} ★') for i in range(1, 11)],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Оценка (1-10)'
    )

    class Meta:
        model = Review
        fields = ['song', 'album', 'rating', 'text', 'is_published']
        widgets = {
            'text': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'form-textarea'}),
            'is_published': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'song': 'Песня',
            'album': 'Альбом',
            'text': 'Текст рецензии',
            'is_published': 'Статус',
        }
        help_texts = {
            'song': 'Выберите песню, если рецензия на песню',
            'album': 'Выберите альбом, если рецензия на альбом',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['song'].empty_label = 'Выберите песню (необязательно)'
        self.fields['album'].empty_label = 'Выберите альбом (необязательно)'
        self.fields['song'].required = False
        self.fields['album'].required = False
        self.fields['text'].validators.append(MinLengthValidator(5, message="Минимум 5 символов"))
        self.fields['text'].validators.append(MaxLengthValidator(300, message="Максимум 300 символов"))


    def clean(self):
        cleaned_data = super().clean()
        song = cleaned_data.get('song')
        album = cleaned_data.get('album')


        if not song and not album:
            raise forms.ValidationError('Рецензия должна быть связана либо с песней, либо с альбомом')


        if song and album:
            raise forms.ValidationError('Рецензия не может быть связана одновременно с песней и альбомом')

        return cleaned_data


