from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True, verbose_name="О себе")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    favorite_artists = models.ManyToManyField(
        'artists.Artist',
        blank=True,
        related_name='fans',
        verbose_name="Любимые исполнители"
    )
    favorite_songs = models.ManyToManyField(
        'music.Song',
        blank=True,
        related_name='fans',
        verbose_name="Любимые песни"
    )
    favorite_albums = models.ManyToManyField(
        'music.Album',
        blank=True,
        related_name='fans',
        verbose_name="Любимые альбомы"
    )

    joined_communities = models.ManyToManyField(
        'communities.Community',
        blank=True,
        related_name='community_members',
        verbose_name="Сообщества"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

