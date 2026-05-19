from django.urls import path
from musicnews import views
urlpatterns = [
    path('', views.NewsAll.as_view(), name = "all_news"),
    path('categories/', views.CategoriesAll.as_view(), name = "categories"),
    path('categories/<slug:category_slug>/', views.NewsByCategoryView.as_view(), name="category"),
    path('add', views.AddNews.as_view(), name="add_news"),
    path('edit/<int:pk>/', views.UpdateNews.as_view(), name="edit_news"),
    path('delete/<int:pk>/', views.DeleteNews.as_view(), name="delete_news"),
]
