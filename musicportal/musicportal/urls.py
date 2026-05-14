from django.contrib import admin
from django.urls import path, include
from homepage import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  include('homepage.urls')),
    path('musicnews/', include('musicnews.urls')),
    path('artists/', include('artists.urls')),
    path('communities/', include('communities.urls')),
    path('reviews/', include('reviews.urls')),
    path('music/', include('music.urls')),
    path('userprofile/<str:username>/', include('userprofile.urls')),

]

handler404 = views.page_not_found
handler403 = views.permission_denied
handler500 = views.server_error

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Музыкальный портал"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

