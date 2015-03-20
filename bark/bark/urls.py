from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from views import views, regviews

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'bark.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),

                       # #PROJECT URLS
                       # #----------
                       #
                       #Main Application Root
                       url(r'^$', views.index, name = 'index'),
                       # #BARK URLS
                       # #----------
                       #
                       # About page
                       url(r'^about/', views.about, name = 'about'),
                       #
                       #
                       # #Generic Post list
                       # Search with tags after, seperated by slashes
                       url(r'^barks/(.*)$', views.viewPosts, name = 'view_posts'),

                       #User Profile View
                       url(r'^users/(?P<username>[\w-]+)', views.userprofile, name="user_profile"),
                       #
                       # #Specific Bark view
                       url(r'^bark/(?P<post_id>[\w-]+)/(?P<post_slug>[\w-]+)/', views.viewPost, name='view_post'),
                       #
                       # #Add new Bark
                       url(r'^new/', views.addPost, name = 'add_post'),
                       #
                       # #Search
                       # #Followed by query string or some form of search regex
                       url(r'^search/', views.search, name = 'search'),

                       url(r'^like_post/$', views.like_post, name='like_post'),
                       url(r'^like_comment/$', views.like_comment, name='like_comment'),
                       #
                       url(r'^follow/(?P<tagName>[\w-]+)', views.follow_tag, name='follow_tag'),
                       # #REGISTRATION VIEWS
                       # #---------
                       #
                       url(r'^signup/', regviews.signup, name = 'signup'),
                       url(r'^signin/', regviews.signin, name = 'signin'),
                       url(r'^signout/', regviews.signout, name = 'signout'),
                       #
                       url(r'^password-change/', regviews.passwordChange, name = 'passwordChange'),
                       url(r'^password-reset/', regviews.passwordReset, name = 'passwordReset'),
                       url(r'^password-reset-do/', regviews.passwordResetCode, name='passwordResetCode'),

                       url(r'^update-profile/', regviews.profileUpdate, name='profile'),
                       )

# Temp bit for uploading profile images during development
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
         'serve',
         {'document_root': settings.MEDIA_ROOT}))
