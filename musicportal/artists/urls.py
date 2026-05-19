from django.urls import path
from artists import views


from django.urls import register_converter,reverse_lazy
from .converters import  YearRangeConverter
register_converter(YearRangeConverter, 'year_range')

urlpatterns = [
    path('genres/', views.CategoriesAll.as_view(), name="genres_for_artists"),
    path('genres/<slug:genre_slug>/', views.ArtistsByGenre.as_view(), name="genre_artist"),
    path('', views.ArtistAll.as_view(), name="all_artists"),
    path('tag/<slug:tag_slug>/',views.show_tag_artistlist, name='tag'),
    path('years/', views.artists_by_years_filter, name="year_artist_filter"),
    path('<year_range:years>/', views.ArtistsByYears.as_view(), name="year_artist"),
    path('add/', views.AddArtist.as_view(), name='add_artist'),
    path('edit/<int:pk>/', views.UpdateArtist.as_view(), name='edit_artist'),
    path('delete/<int:pk>/', views.DeleteArtist.as_view(), name='delete_artist'),
]

