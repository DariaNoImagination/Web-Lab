from django import template
from communities.models import Community
from artists.models import TagPost
register = template.Library()

@register.inclusion_tag('list_communities.html')
def show_categories():
    communities = Community.objects.all()
    return {"communities": communities}

@register.inclusion_tag('list_tags.html')
def show_all_tags():
 return {"tags": TagPost.objects.all()}
