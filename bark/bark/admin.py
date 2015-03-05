from models import *
from django.contrib import admin


admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(PostTagging)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(PostLike)
admin.site.register(CommentLike)
admin.site.register(Tag)
admin.site.register(InstitutionTag)
admin.site.register(UserTag)
admin.site.register(TagFollowing)

