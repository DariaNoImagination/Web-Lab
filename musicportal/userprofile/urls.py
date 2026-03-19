from django.urls import path
from userprofile import views
urlpatterns = [
    path('', views.user_profile, name = "profile"),
    path('edit/', views.edit_profile, name = "profile_edit"),
]
