from django.urls import path
from music import views
urlpatterns = [
    path('', views.about_music, name = "all_music"),
]
