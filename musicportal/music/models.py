from django.db import models

class Song(models.Model):
    artist = models.CharField(max_length=255, verbose_name="Исполнитель")
    title = models.CharField(max_length=255, verbose_name="Название песни")
    album = models.CharField(max_length=255, verbose_name="Альбом", blank=True, null=True)
    year = models.IntegerField(verbose_name="Год выпуска")
    genre = models.CharField(max_length=100, verbose_name="Жанр", blank=True, null=True)

    class Meta:
        verbose_name = "Песня"
        verbose_name_plural = "Песни"
        ordering = ['-year', 'title']

    def __str__(self):
        return f"{self.title} - {self.artist}"


class Album(models.Model):
    artist = models.CharField(max_length=255, verbose_name="Исполнитель")
    title = models.CharField(max_length=255, verbose_name="Название альбома")
    year = models.IntegerField(verbose_name="Год выпуска")
    genre = models.CharField(max_length=100, verbose_name="Жанр", blank=True, null=True)
    songs_count = models.IntegerField(verbose_name="Количество песен", blank=True, null=True)

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"
        ordering = ['-year', 'title']

    def __str__(self):
        return f"{self.title} - {self.artist}"