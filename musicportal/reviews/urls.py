from django.urls import path
from reviews import views
urlpatterns = [
    path('', views.index, name = "all_reviews"),
    path('genres/', views.categories, name="genres_for_reviews"),
    path('genres/<slug:genre_slug>/', views.reviews_by_genre, name="genre_reviews"),
    path('comment/<int:review_id>/', views.addcomment, name='add_comment_url'),
    path('add/', views.add_review, name='add_review'),
]
