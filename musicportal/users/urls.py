from django.urls import path
from django.urls import reverse_lazy
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
     path('login/', views.LoginUser.as_view(), name='login'),
     path('logout/', LogoutView.as_view(next_page=reverse_lazy('main')), name='logout'),

]

app_name = "users"