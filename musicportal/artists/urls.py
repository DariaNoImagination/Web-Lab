from django.urls import path
from artists import views

urlpatterns = [
    path('genres/', views.categories, name="genres_for_artists"),
    path('genres/<slug:genre_slug>/', views.artists_by_genre, name="genre_artist"),
    path('', views.index, name="all_artists"),
]