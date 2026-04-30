from django.contrib import admin

# Register your models here.
from .models import Artist,Genre,TagPost

@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):

    list_display = ('id', 'tag', 'slug')
    list_display_links = ('id', 'tag')
    list_editable = ('slug',)
    ordering = ['tag']
    search_fields = ['tag', 'slug']
    list_per_page = 20
    list_filter = ('tag',)
    prepopulated_fields = {'slug': ('tag',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title')
    list_editable = ('slug',)
    ordering = ['title']
    search_fields = ['title', 'slug']
    list_per_page = 20
    list_filter = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'get_genre',
        'active_from',
        'active_to',
        'get_career_length',
        'get_tags'
    )
    list_display_links = ('id', 'title')
    list_editable = ('active_from', 'active_to')
    ordering = ['-active_from', 'title']
    search_fields = ['title', 'content', 'genre__title']
    list_per_page = 15

    class ActivityFilter(admin.SimpleListFilter):
        title = 'Деятельность исполнителей'
        parameter_name = 'activity'

        def lookups(self, request, model_admin):
            return [
                ('active', 'Продолжают карьеру'),
                ('inactive', 'Завершили карьеру'),
            ]
        def queryset(self, request, queryset):
            if self.value() == 'active':
                return queryset.filter(active_to__isnull=True)
            elif self.value() == 'inactive':
                return  queryset.filter(active_to__isnull=False)

    list_filter = ('genre', 'tags',ActivityFilter)
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'genre', 'content')
        }),
        ('Период активности', {
            'fields': ('active_from', 'active_to'),
            'classes': ('wide',)
        }),
        ('Теги', {
            'fields': ('tags',),
            'description': 'Выберите теги для исполнителя'
        }),
    )
    filter_horizontal = ('tags',)

    def get_genre(self, obj):
        return obj.genre.title

    get_genre.short_description = 'Жанр'
    get_genre.admin_order_field = 'genre__title'

    @admin.display(description="Длительность карьеры")
    def get_career_length(self, obj):
        if obj.active_from:
            end = obj.active_to if obj.active_to else 2026
            return f"{end - obj.active_from} лет"
        return "—"




    def get_tags(self, obj):
        return ", ".join([tag.tag for tag in obj.tags.all()])

    get_tags.short_description = 'Теги'

    actions = ['set_active', 'set_inactive']

