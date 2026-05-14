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

class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100, verbose_name="Автор")
    text = models.TextField(verbose_name="Текст комментария")
    rating = models.IntegerField(verbose_name="Оценка рецензии",null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=True, verbose_name="Опубликован")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author}: {self.text[:50]}"
