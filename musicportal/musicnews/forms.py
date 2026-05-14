from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .models import News


class AddNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'category', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите заголовок новости'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'content': forms.Textarea(attrs={
                'cols': 60,
                'rows': 10,
                'class': 'form-textarea',
                'placeholder': 'Введите текст новости...'
            }),
        }
        labels = {
            'title': 'Заголовок',
            'category': 'Категория',
            'content': 'Содержание',
        }
        help_texts = {
            'title': 'Введите заголовок новости (минимум 5 символов)',
            'category': 'Выберите категорию новости',
            'content': 'Подробное описание новости',
        }
        error_messages = {
            'title': {
                'required': 'Пожалуйста, введите заголовок',
                'max_length': 'Заголовок не должен превышать 255 символов',
            },
            'category': {
                'required': 'Выберите категорию',
                'invalid_choice': 'Выберите корректную категорию',
            },
            'content': {
                'required': 'Пожалуйста, введите содержание новости',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.fields['title'].validators.append(
            MinLengthValidator(5, message="Заголовок должен содержать минимум 5 символов")
        )
        self.fields['title'].validators.append(
            MaxLengthValidator(255, message="Заголовок не должен превышать 255 символов")
        )


        self.fields['content'].validators.append(
            MinLengthValidator(20, message="Содержание должно содержать минимум 20 символов")
        )
        self.fields['content'].validators.append(
            MaxLengthValidator(10000, message="Содержание не должно превышать 10000 символов")
        )

        # Добавляем пустую опцию для категории
        self.fields['category'].empty_label = 'Выберите категорию'
        self.fields['category'].required = True

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            title = ' '.join(title.split())
            if News.objects.filter(title__iexact=title).exists():
                if not self.instance.pk or self.instance.title != title:
                    raise forms.ValidationError('Новость с таким заголовком уже существует')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content:
            if len(content.strip()) < 20:
                raise forms.ValidationError('Содержание новости слишком короткое')
        return content