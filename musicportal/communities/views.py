from django.shortcuts import render,redirect
from .forms import AddCommunityForm
def index(request):

    data = {
        'title': 'Сообщества фанатов',
    }
    return render(request, 'information.html',
                  context=data)

def add_community(request):
    if request.method == 'POST':
        form = AddCommunityForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('all_communities')
    else:
        form = AddCommunityForm()

    return render(request, 'generic_form.html', {
        'form': form,
        'title': 'Добавление сообщества',
        'button_text': 'Добавить'
    })


