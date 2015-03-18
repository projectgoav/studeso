from django import template
from bark.models import Post, Tag

register = template.Library()

@register.inclusion_tag('bark/postlist.html')
def get_view(post):
    return {'post' : post }
