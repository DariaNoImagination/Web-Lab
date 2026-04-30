from django.contrib import admin,messages

# Register your models here.
from .models import Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_content',
        'get_artist',
        'rating',
        'date',
        'is_published',
        'get_review_preview'
    )

    list_display_links = ('id', 'get_content')
    list_filter = ('is_published', 'rating', 'date')
    search_fields = ('text', 'song__title', 'album__title', 'song__artist__title', 'album__artist__title')
    list_per_page = 20

    fieldsets = (
        ('Информация о рецензии', {
            'fields': ('rating', 'text', 'date', 'is_published')
        }),
        ('Связанный контент', {
            'fields': ('song', 'album'),
            'description': 'Рецензия может быть либо на песню, либо на альбом'
        }),
    )
    actions = ['set_published', 'set_draft']

    def get_content(self, obj):
        if obj.song:
            return obj.song.title
        elif obj.album:
            return obj.album.title
        return "—"

    get_content.short_description = 'Название'

    def get_artist(self, obj):
        if obj.song and obj.song.artist:
            return obj.song.artist.title
        elif obj.album and obj.album.artist:
            return obj.album.artist.title
        return "—"

    get_artist.short_description = 'Исполнитель'
    get_artist.admin_order_field = 'song__artist__title'

    def get_review_preview(self, obj):
        if obj.text:
            return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
        return "—"

    get_review_preview.short_description = 'Текст (превью)'  # ← ДОБАВИТЬ ЭТО!


    @admin.action(description="Опубликовать выбранные рецензии")
    def set_published(self, request, queryset):
        count = queryset.update(is_published= Review.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} рецензий.")

    @admin.action(description="Снять с публикации выбранные рецензии")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Review.Status.DRAFT)
        self.message_user(request, f"{count} рецензий сняты с публикации!", messages.WARNING)
