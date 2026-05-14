from django.urls import path
from communities import views
urlpatterns = [
    path('', views.index, name = "all_communities"),
    path('add/', views.add_community, name='add_community'),
]
