from django.urls import path
from communities import views
urlpatterns = [
    path('', views.CommunityAll.as_view(), name = "all_communities"),
    path('add/', views.AddCommunity.as_view(), name='add_community'),
    path('edit/<int:pk>/', views.UpdateCommunity.as_view(), name='edit_community'),
    path('delete/<int:pk>/', views.DeleteCommunity.as_view(), name='delete_community'),
]
