from django import template
from communities.models import Community

register = template.Library()

@register.inclusion_tag('list_communities.html')
def show_categories():
    communities = Community.objects.all()
    return {"communities": communities}