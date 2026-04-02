from django.db import models

class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Review.Status.PUBLISHED)

class Review(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    TYPE_CHOICES = [
        ('album', 'Альбом'),
        ('song', 'Песня'),
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Тип рецензии")
    title = models.CharField(max_length=255, verbose_name="Название")
    artist = models.CharField(max_length=255, verbose_name="Исполнитель")
    genre = models.CharField(max_length=10, verbose_name="Жанр")
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

    def __str__(self):
        return f"{self.get_type_display()}: {self.title}"