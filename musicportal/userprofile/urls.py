from django.urls import path
from userprofile import views
urlpatterns = [
    path('', views.UserProfile.as_view(), name = "profile"),
    path('edit/', views.edit_profile, name = "profile_edit"),
    path('review/edit/<int:pk>/', views.UpdateReview.as_view(),name='edit_review'),
    path('review/delete/<int:pk>/', views.DeleteReview.as_view(),name='delete_review'),
]
