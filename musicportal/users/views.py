from django.urls import reverse_lazy
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from users.forms import LoginUserForm,RegisterUserForm
from django.views.generic.edit import CreateView
from .forms import UserPasswordChangeForm
from django.contrib.auth.views import PasswordChangeView

@method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'
    extra_context = {'title': "Авторизация"}

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('main')

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    extra_context = {'title': "Регистрация"}
    def get_success_url(self):
        return reverse_lazy('users:login')


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("userprofile:password_change_done")
    template_name = "password_change_form.html"
    extra_context = {'title': "Изменение пароля"}


