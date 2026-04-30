from django.contrib import admin

# Register your models here.
from .models import News
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_at','content','brief_info')
    search_fields = ('title',)
    @admin.display(description="Краткое описание")
    def brief_info(self, news: News):
            return f" {len(news.content)} символов"
