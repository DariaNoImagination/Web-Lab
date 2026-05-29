from django.urls import reverse_lazy
from .forms import AddCommunityForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView,DeleteView

from .models import Community


class CommunityAll(ListView):
    model = Community
    template_name = 'information.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Community.objects.all().order_by('-members')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Сообщества фанатов'
        context['app_name'] = 'communities'

        page_obj = context.get('page_obj')
        paginator = context.get('paginator')

        if paginator:
            context['page_range'] = paginator.page_range
        context['is_paginated'] = paginator.num_pages > 1

        return context



class AddCommunity(CreateView):
    form_class = AddCommunityForm
    template_name = 'generic_form.html'
    success_url = reverse_lazy('all_communities')
    extra_context = {'title': 'Добавление сообщества','button_text': 'Добавить сообщество'}

class UpdateCommunity(UpdateView):
    model = Community
    form_class = AddCommunityForm
    template_name = 'generic_form.html'
    extra_context = {'title': 'Редактировать сообщество',
                     'button_text': 'Сохранить изменения'}
    success_url = reverse_lazy('all_communities')

class DeleteCommunity(DeleteView):
    model = Community
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('all_communities')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление сообщества'
        context['object_type'] = 'сообщество'
        context['object_title'] = self.object.club_name
        context['cancel_url'] = reverse_lazy('all_communities')
        return context





