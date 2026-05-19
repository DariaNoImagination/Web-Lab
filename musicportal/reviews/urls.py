from django.urls import path
from reviews import views
urlpatterns = [
    path('', views.ReviewsAll.as_view(), name = "all_reviews"),
    path('genres/', views.ReviewsCategoriesView.as_view(), name="genres_for_reviews"),
    path('genres/<slug:genre_slug>/', views.ReviewsByGenreView.as_view(), name="genre_reviews"),
    path('comment/<int:review_id>/', views.AddComment.as_view(), name='add_comment_url'),
    path('add/', views.AddReview.as_view(), name='add_review'),

]
