from django.urls import path
from musicnews import views
urlpatterns = [
    path('', views.index, name = "all_news"),
    path('categories/', views.categories, name = "categories"),
    path('categories/<slug:category_slug>/', views.news_by_category, name="category"),
]
