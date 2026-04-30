from django.db import models
from music.models import Album,Song

class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Review.Status.PUBLISHED)

class Review(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    song = models.ForeignKey(Song, on_delete=models.DO_NOTHING, default= None, null=True,blank=True, verbose_name= "Песня")
    album = models.ForeignKey(Album,on_delete=models.DO_NOTHING, default= None, null=True, blank=True, verbose_name= "Альбом")
    rating = models.IntegerField(verbose_name="Рейтинг")
    text = models.TextField(verbose_name="Текст рецензии")
    date = models.CharField(max_length=50, verbose_name="Дата публикации")
    is_published =  models.BooleanField(choices=Status.choices,default=Status.DRAFT)
    objects = models.Manager()
    published = PublishedModel()

    class Meta:
        verbose_name = "Рецензия"
        verbose_name_plural = "Рецензии"
        ordering = ['-date']


