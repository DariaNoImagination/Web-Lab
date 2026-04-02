from django.shortcuts import render
from musicnews.models import News

category_names = {
        'events': 'Концерты и события',
        'awards': 'Премии и награды',
        'new': 'Новинки музыки',
    }

def index(request):
    news = News.objects.all()
    data = {
        'title': 'Все новости музыки',
        'news': news,
        'show_all': True,
    }
    return render(request, 'news.html', context=data)

def categories(request):
    data = {
        'title': 'Категории музыкальных новостей',
        'categories': category_names.values()
    }
    return render(request, 'categories.html',
                  context=data)


def news_by_category(request, category_slug):
    news = News.objects.all()
    filtered_news = [news for news in news if news.category == category_slug]

    category_name = category_names.get(category_slug, category_slug)

    data = {
        'title': f'Новости: {category_name}',
        'news': filtered_news,
        'category_slug': category_slug,
    }

    return render(request, 'news.html', context=data)



