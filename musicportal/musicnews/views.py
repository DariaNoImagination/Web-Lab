from musicnews.models import News
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .forms import AddNewsForm
from django.views.generic import ListView,TemplateView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy

category_names = {
        'events': 'Концерты и события',
        'awards': 'Премии и награды',
        'new': 'Новинки музыки',
    }


class NewsAll(ListView):
    model = News
    template_name = 'news.html'
    context_object_name = 'news'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все новости музыки'
        context['show_all'] = True
        return context


class CategoriesAll(TemplateView):
    template_name = 'categories.html'
    extra_context = {
        'title': 'Категории музыкальных новостей',
        'categories': category_names.values()
    }


class NewsByCategoryView(ListView):
    model = News
    template_name = 'news.html'
    context_object_name = 'news'

    def dispatch(self, request, *args, **kwargs):
        self.category_slug = kwargs['category_slug']
        self.category_name = category_names.get(self.category_slug, self.category_slug)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        week_ago = timezone.now() - timedelta(days=7)
        return News.objects.filter(
            Q(category=self.category_slug) &
            Q(created_at__gte=week_ago)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Новости: {self.category_name}'
        context['category_slug'] = self.category_slug
        return context


class AddNews(CreateView):
    form_class = AddNewsForm
    template_name = 'generic_form.html'
    success_url = reverse_lazy('all_news')
    extra_context = {'title': 'Добавление новости','button_text': 'Добавить новость'}

class UpdateNews(UpdateView):
    model = News
    fields = ['title', 'category', 'content']
    template_name = 'generic_form.html'
    success_url = reverse_lazy('all_news')
    extra_context = {'title': 'Редактирование новости','button_text': 'Сохранить изменения'}

class DeleteNews(DeleteView):
    model = News
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('all_news')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = super().delete(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление новости'
        context['object_type'] = 'новость'
        context['object_title'] = self.object.title
        context['cancel_url'] = reverse_lazy('all_news')
        return context