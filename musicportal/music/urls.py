from django.urls import path
from music import views
urlpatterns = [
    path('', views.AboutMusic.as_view(), name = "all_music"),
    path('filter/', views.FilterMusicView.as_view(), name='filter_music'),
    path('add/song/', views.AddSong.as_view(), name='add_song'),
    path('add/album', views.AddAlbum.as_view(), name='add_album'),
    path('update/song/<int:pk>/', views.UpdateSong.as_view(), name='update_song'),
    path('update/album/<int:pk>/', views.UpdateAlbum.as_view(), name='update_album'),
    path('delete/song/<int:pk>/', views.DeleteSong.as_view(), name='delete_song'),
    path('delete/album/<int:pk>/', views.DeleteAlbum.as_view(), name='delete_album'),
]
