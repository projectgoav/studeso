from django import template
from bark.models import UserTag, InstitutionTag, Tag

register = template.Library()

@register.inclusion_tag('sidebar.html')
def get_sidebar():
    user_tags = UserTag.objects.all()
    inst_tags = InstitutionTag.objects.all()
    other_tags = []

    tags = Tag.objects.all()
    for t in tags:
        if t not in user_tags and t not in inst_tags:
            other_tags += [t]

    return {'U' : user_tags, 'I' : inst_tags, 'A' : other_tags }
