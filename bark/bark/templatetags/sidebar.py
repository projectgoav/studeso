from django import template
from bark.models import UserTag, InstitutionTag, Tag

register = template.Library()

@register.inclusion_tag('sidebar.html')
def get_sidebar(is_auth):

    tags = Tag.objects.all().exclude(id__in=UserTag.objects.all()).exclude(id__in=InstitutionTag.objects.all())
    users =  Tag.objects.all().filter(id__in=UserTag.objects.all())
    inst = Tag.objects.all().filter(id__in=InstitutionTag.objects.all())

    if is_auth == True:
        followed = [ ]

        if (len(followed) == 0):
            return { 'U' : users, 'I' : inst, 'A' : tags, 'F' : followed, 'FE' : { }}
        return { 'U' : users, 'I' : inst, 'A' : tags, 'F' : followed}
    return {'U' : users, 'I' : inst, 'A' : tags }
