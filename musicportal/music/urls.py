from django.urls import path
from music import views
urlpatterns = [
    path('', views.about_music, name = "all_music"),
    path('filter/', views.filter_music, name='filter_music'),
    path('add/song/', views.add_song, name='add_song'),
    path('add/album', views.add_album, name='add_album'),
]
