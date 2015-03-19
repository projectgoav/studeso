from django import template
from bark.models import Post, Tag

register = template.Library()

@register.inclusion_tag('bark/postlist.html')
def get_view(post):
    context_dictionary = {}

    tags = post.tags.exclude(name__iexact=post.author.user_tag.name
                             ).exclude(name__iexact=post.author.institution_tag.name)

    context_dictionary['post'] = post
    context_dictionary['post_tags'] = tags
    context_dictionary['post_likes'] = post.postlike_set.count()

    if post.tags.filter(name=post.author.institution_tag.name).exists():
        context_dictionary['post_inst_tag'] = post.author.institution_tag

    return context_dictionary
