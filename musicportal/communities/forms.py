from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from .models import Community


class AddCommunityForm(forms.ModelForm):
    members = forms.IntegerField(
        min_value=1,
        max_value=1000000000,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'например: 1500'}),
        label='Количество участников',
        help_text='Введите количество участников фан-клуба (от 1 до 1 000 000 000)',
        validators=[
            MinValueValidator(1, message="Количество участников не может быть меньше 1"),
            MaxValueValidator(1000000000, message="Количество участников не может превышать 1 000 000 000")
        ]
    )

    class Meta:
        model = Community
        fields = ['artist', 'club_name', 'founded', 'members', 'description']
        widgets = {
            'club_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите название фан-клуба'
            }),
            'artist': forms.Select(attrs={'class': 'form-select'}),
            'founded': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'например: 2010 год или 15 марта 2009'
            }),
            'description': forms.Textarea(attrs={
                'cols': 60,
                'rows': 8,
                'class': 'form-textarea',
                'placeholder': 'Расскажите о фан-клубе...'
            }),
        }
        labels = {
            'artist': 'Исполнитель',
            'club_name': 'Название фан-клуба',
            'founded': 'Дата основания',
            'members': 'Количество участников',
            'description': 'Описание',
        }
        help_texts = {
            'artist': 'Выберите исполнителя, к которому относится фан-клуб',
            'club_name': 'Введите официальное название фан-клуба',
            'founded': 'Укажите год или полную дату основания',
            'description': 'Краткое описание деятельности фан-клуба',
        }
        error_messages = {
            'club_name': {
                'required': 'Пожалуйста, введите название фан-клуба',
                'max_length': 'Название не должно превышать 255 символов',
            },
            'members': {
                'required': 'Пожалуйста, укажите количество участников',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['artist'].empty_label = 'Выберите исполнителя'
        self.fields['artist'].required = False


        self.fields['description'].validators.append(
            MinLengthValidator(10, message="Минимум 10 символов")
        )
        self.fields['description'].validators.append(
            MaxLengthValidator(5000, message="Максимум 5000 символов")
        )


        self.fields['club_name'].validators.append(
            MinLengthValidator(2, message="Минимум 2 символа")
        )

    def clean_club_name(self):
        """Валидация названия фан-клуба"""
        club_name = self.cleaned_data.get('club_name')
        if club_name:

            if Community.objects.filter(club_name__iexact=club_name).exists():
                if not self.instance.pk or self.instance.club_name != club_name:
                    raise forms.ValidationError('Фан-клуб с таким названием уже существует')

            club_name = ' '.join(club_name.split())
        return club_name

    def clean_founded(self):
        founded = self.cleaned_data.get('founded')
        if founded:
            if len(founded) < 3:
                raise forms.ValidationError('Введите корректную дату основания')
        return founded

    def clean(self):
        cleaned_data = super().clean()
        members = cleaned_data.get('members')
        if members and members < 0:
            raise forms.ValidationError('Количество участников не может быть отрицательным')
        return cleaned_data