from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [ path('profile/', views.ProfileUser.as_view(), name = "profile"),
     path('review/edit/<int:pk>/', views.UpdateReview.as_view(), name='edit_review'),
     path('review/delete/<int:pk>/', views.DeleteReview.as_view(), name='delete_review'),
     path('favorite/artist/toggle/<int:pk>/', views.ToggleFavoriteArtistView.as_view(),
          name='toggle_favorite_artist'),
     path('favorite/artists/', views.FavoriteArtistsListView.as_view(), name='favorite_artists'),
     path('favorite/song/toggle/<int:pk>/', views.ToggleFavoriteSongView.as_view(), name='toggle_favorite_song'),
     path('favorite/songs/', views.FavoriteSongsListView.as_view(), name='favorite_songs'),
     path('favorite/album/toggle/<int:pk>/', views.ToggleFavoriteAlbumView.as_view(), name='toggle_favorite_album'),
     path('favorite/albums/', views.FavoriteAlbumsListView.as_view(), name='favorite_albums'),

     path('community/toggle/<int:pk>/', views.ToggleCommunityView.as_view(), name='toggle_community'),
     path('communities/', views.JoinedCommunitiesListView.as_view(), name='joined_communities'),]

