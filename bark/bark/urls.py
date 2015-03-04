from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from bark.views import views, regviews

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bark.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    	#PROJECT URLS
    	#----------

		#Main Application Root
        url(r'^$', views.index, name = 'index'),

        #Just redirect back to homepage?
        #TODO
        url(r'^bark/' views.index, name = 'barkIndex'),

		#BARK URLS
		#----------

        #Generic Post list
        # TODO
        # Add tags as /TAG/TAG/TAG to filter depending on the tags
        url(r'^bark/tags/', views.barks, name = 'barks'),

        #Specific Bark view
        url(r'^bark/<post_id>/', views.barkview, name = 'barkview'),
       
        #Add new Bark
        url(r'^bark/new/', views.addbark, name = 'addbark'),

        #Search
        #Followed by query string or some form of search regex
        url(r'^search/', views.search, name = 'search'),


        #UUSER PROFILE FILES
        #---------------

        #Displays list of users
        #Ranked by helpfulness?
        #TODO
        url(r'^users/', regviews.users, name = 'users'),

        #Displays specific user profile
        url(r'^users/<user_name>/', regviews.viewuser, name = 'viewuser'),

        #PERSONAL PROFILE VIEWS
        #------------

        #View your own profile, when logged in
        url(r'^profile/', regviews.profile, name = "profile"),

        #Update your profile information
        url(r'^profile/update/', regviews.profileUpdate, name = 'profileUpdate'),


        #REGISTRATION VIEWS
        #---------

        url(r'^signup/', regviews.signup, name = 'signup'),
        url(r'^signin/', regviews.signin, name = 'signin'),
        url(r'^signout/', regviews.signout, name = 'signout'),

        url(r'^password/', regviews.passwordMenu, name = 'passwordMenu'),
        url(r'^password/change/', regviews.passwordChange, name = 'passwordChange'),
        url(r'^password/reset/', regviews.passwordReset, name = 'passwordReset'),
)

# Temp bit fo uploading profile images during developement
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), 
