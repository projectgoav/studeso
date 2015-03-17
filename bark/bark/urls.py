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
                       # Help page
                       url(r'^help/', views.help, name = 'help'),
                       #
                       # #Generic Post list
                       # TODO
                       # Add tags as /TAG/TAG/TAG to filter depending on the tags
                       url(r'^barks/(?P<tag_id>[\w-]+)', views.viewPosts, name = 'view_posts'),
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

                       url(r'^suggest_tags/$', views.suggest_tags, name='suggest_tags'),

                       url(r'^like_post/$', views.like_post, name='like_post'),
                       #
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

                       url(r'^profile/', regviews.profileUpdate, name='profile'),
                       )

# Temp bit for uploading profile images during development
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
         'serve',
         {'document_root': settings.MEDIA_ROOT}))
