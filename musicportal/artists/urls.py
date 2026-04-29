from django.urls import path
from artists import views

urlpatterns = [
    path('genres/', views.categories, name="genres_for_artists"),
    path('genres/<slug:genre_slug>/', views.artists_by_genre, name="genre_artist"),
    path('', views.index, name="all_artists"),
    path('tag/<slug:tag_slug>/',views.show_tag_artistlist, name='tag'),
    path('years/', views.artists_by_years_filter, name="year_artist_filter"),
    path('<year_range:years>/', views.artists_by_years, name="year_artist"),
]

