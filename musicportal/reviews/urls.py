from django.urls import path
from reviews import views

app_name = 'reviews'

urlpatterns = [
    path('', views.ReviewsAll.as_view(), name = "all_reviews"),
    path('edit/<int:pk>/', views.UpdateReview.as_view(), name='edit_review'),
    path('delete/<int:pk>/', views.DeleteReview.as_view(), name='delete_review'),
    path('genres/', views.ReviewsCategoriesView.as_view(), name="genres_for_reviews"),
    path('genres/<slug:genre_slug>/', views.ReviewsByGenreView.as_view(), name="genre_reviews"),
    path('comment/add/<int:review_id>/', views.AddComment.as_view(), name='add_comment_url'),
    path('comment/edit/<int:pk>/', views.UpdateComment.as_view(), name='edit_comment_url'),
    path('comment/delete/<int:pk>/', views.DeleteComment.as_view(), name='delete_comment_url'),
    path('add/', views.AddReview.as_view(), name='add_review'),

]
