from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
        'display_avatar'
    )

    list_display_links = ('id', 'username')
    list_editable = ('is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_per_page = 20

    fieldsets = (
        ('Основная информация', {
            'fields': ('username', 'email', 'first_name', 'last_name', 'password')
        }),
        ('Личная информация', {
            'fields': ('bio', 'avatar', 'birth_date'),
            'classes': ('wide',)
        }),
        ('Избранное', {
            'fields': ('favorite_artists', 'favorite_songs', 'favorite_albums', 'joined_communities'),
            'description': 'Любимые исполнители, песни, альбомы и сообщества пользователя'
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Важные даты', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = (
        'favorite_artists',
        'favorite_songs',
        'favorite_albums',
        'joined_communities',
        'groups',
        'user_permissions'
    )

    def display_avatar(self, obj):
        if obj.avatar:
            return mark_safe(
                f'<img src="{obj.avatar.url}" width="50" height="50" style="border-radius: 50%; object-fit: cover;">')
        return "Нет аватара"

    display_avatar.short_description = 'Аватар'