
from django.db import models

class News(models.Model):
    CATEGORY_CHOICES = [
        ('awards', 'Премии'),
        ('events', 'Концерты/мероприятия'),
        ('new', 'Новинки'),
    ]

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Категория")
    content = models.TextField(verbose_name="Содержание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


