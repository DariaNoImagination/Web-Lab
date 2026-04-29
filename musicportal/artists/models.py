from django.db import models
from django.urls import reverse


class TagPost(models.Model):
    tag = models.CharField(max_length=100,
                           db_index=True)
    slug = models.SlugField(max_length=255,
                            unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug':
    self.slug})

    def __str__(self):
        return self.tag



class Genre(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255,unique=True, db_index=True, verbose_name="URL", blank=True, default='')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('genre_artist', kwargs={'genre_slug': self.slug})



class Artist(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre,on_delete=models.PROTECT, default = 1)
    content = models.TextField(blank=True)
    tags = models.ManyToManyField('TagPost', blank=True, related_name='artists')
    active_from = models.IntegerField(null=True, blank=True)
    active_to = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title





