from django.contrib import admin

# Register your models here.
from .models import Community


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('club_name', 'get_artist', 'members', 'founded',"description")
    list_display_links = ('club_name',)
    list_editable = ('members',)
    list_filter = ('founded',)
    search_fields = ('club_name', 'artist__title')
    list_per_page = 20

    def get_artist(self, obj):
        return obj.artist.title if obj.artist else "—"

    get_artist.short_description = 'Исполнитель'