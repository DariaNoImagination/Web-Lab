from django.db import models
from artists.models import Artist,Genre

from django.db.models import Avg
class Album(models.Model):
    artist = models.ForeignKey(Artist,on_delete=models.CASCADE,default = 1)
    title = models.CharField(max_length=255, verbose_name="Название альбома")
    year = models.IntegerField(verbose_name="Год выпуска")
    genre = models.ForeignKey(Genre,on_delete=models.PROTECT, default = 1)
    songs_count = models.IntegerField(verbose_name="Количество песен", blank=True, null=True)

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"
        ordering = ['-year', 'title']

    def __str__(self):
        return f"{self.title} "

    def get_avg_rating(self):
        from reviews.models import Review
        return self.review_set.filter(
            is_published=Review.Status.PUBLISHED
        ).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating'] or 0


class Song(models.Model):
    artist = models.ForeignKey(Artist,on_delete=models.CASCADE,default = 1)
    title = models.CharField(max_length=255, verbose_name="Название песни")
    album= models.ForeignKey(Album,on_delete=models.CASCADE, default = 1)
    year = models.IntegerField(verbose_name="Год выпуска")
    genre = models.ForeignKey(Genre,on_delete=models.PROTECT, default = 1)

    class Meta:
        verbose_name = "Песня"
        verbose_name_plural = "Песни"
        ordering = ['-year', 'title']


    def __str__(self):
        return f"{self.title}"

    def get_avg_rating(self):
        from reviews.models import Review
        return self.review_set.filter(
            is_published=Review.Status.PUBLISHED
        ).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating'] or 0

