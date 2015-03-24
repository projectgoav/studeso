from django import template
from bark.models import UserTag, InstitutionTag, Tag, TagFollowing, UserProfile

register = template.Library()

# Provides the List of Tags at the side for users
# Sidebar varies depending on the state of the user and if one is logged in or not.
@register.inclusion_tag('sidebar.html')
def get_sidebar(user):

    #Get all the tags Bark has knowledge off, splitting them into types
    tags = Tag.objects.all().exclude(id__in=UserTag.objects.all()).exclude(id__in=InstitutionTag.objects.all())
    users =  Tag.objects.all().filter(id__in=UserTag.objects.all())
    inst = Tag.objects.all().filter(id__in=InstitutionTag.objects.all())

    #Getting if the user has logged in
    if user.is_authenticated():
        user_profile = UserProfile.objects.get(user=user)
        f_tags = TagFollowing.objects.all().filter(user=user_profile)
        followed = [ ]

        #Get all the tags they follow, if any, and add them to a dictionary for template making special note of the colours
        for tag in f_tags:
            t_dic = { }
            tag_o = Tag.objects.get(id=tag.tag_id)
            t_dic['name'] = tag_o.name

            if tag_o in users:
                t_dic['color'] = "user"
            elif tag_o in inst:
                t_dic['color'] = "inst"
            followed.append(t_dic)

    #Many happy returns
        if (len(followed) == 0):
            return { 'UserTags' : users, 'InstTags' : inst, 'AllTags' : tags, 'FollowedTags' : followed, 'FE' : { }}
        else:
            return { 'UserTags' : users, 'InstTags' : inst, 'AllTags' : tags, 'FollowedTags' : followed}

    return {'UserTags' : users, 'InstTags' : inst, 'AllTags' : tags }
