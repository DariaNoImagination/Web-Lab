from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(
        disabled=True,
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    email = forms.CharField(
        disabled=True,
        label='Email',
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'bio': 'О себе',

        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-textarea'}),

        }



