from django.db import models
from django.urls import reverse


class TagPost(models.Model):
    tag = models.CharField(max_length=100,
                           db_index=True, verbose_name="Тег")
    slug = models.SlugField(max_length=255,
                            unique=True, db_index=True, verbose_name="URL")

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug':
    self.slug})

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.tag



class Genre(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255,unique=True, db_index=True, verbose_name="URL", blank=True, default='')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def get_absolute_url(self):
        return reverse('genre_artist', kwargs={'genre_slug': self.slug})



class Artist(models.Model):
    title = models.CharField(max_length=255, verbose_name="Исполнитель")
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, default=1, verbose_name="Жанр")
    content = models.TextField(blank=True, verbose_name="Описание")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='artists', verbose_name="Теги")
    active_from = models.IntegerField(null=True, blank=True, verbose_name="Активен с")
    active_to = models.IntegerField(null=True, blank=True, verbose_name="Активен по")

    class Meta:
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"

    def __str__(self):
        return self.title





