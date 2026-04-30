from django.db import models
from artists.models import Artist
class Community(models.Model):
    artist = models.OneToOneField( Artist,on_delete=models.SET_NULL, null=True, blank=True,verbose_name="Исполнитель")
    club_name = models.CharField(max_length=255, verbose_name="Название фан-клуба")
    founded = models.CharField(max_length=255, verbose_name="Дата основания")
    members = models.IntegerField(verbose_name="Количество участников",)
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Фан-клуб"
        verbose_name_plural = "Фан-клубы"
        ordering = ['-members']

    def __str__(self):
        return f"{self.club_name} - {self.artist}"


