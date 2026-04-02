from django.db import models
from django.urls import reverse

class Genre(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255,unique=True, db_index=True, verbose_name="URL", blank=True, default='')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('genre_artist', kwargs={'genre_slug': self.slug})



class Artist(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=10)
    content = models.TextField(blank=True)
    active_years  = models.CharField(null=True, blank=True)

    def __str__(self):
        return self.title



