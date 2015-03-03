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
        url(r'^$', views.index, name='index'),

        #Just redirect back to homepage?
        #TODO
        url(r'^bark/' views.index, name='Barkindex'),

		#BARK URLS
		#----------

        #Generic Post list
        #TODO
        #Add tags as /TAG/TAG/TAG to filter depending on the tags
        url(r'^bark/tags/', views.posts, name='posts'),

        #Specific Bark view
        url(r'^bark/<post_id>/', views.postview, name ='postview'),
       
        #Add new Bark
        url(r'^bark/new/', views.addbark, name='addbark'),

        #Search
        #Followed by query string or some form of search regex
        url(r'^search/', views.search, name='search'),


        #UUSER PROFILE FILES
        #---------------

        #Displays list of users
        #Ranked by helpfulness?
        #TODO
        url(r'^users/', regviews.users, name='users'),

        #Displays specific user profile
        url(r'^users/<user_name>/', regviews.profile, name='profile'),

        #PERSONAL PROFILE VIEWS
        #------------

        #View your own profile, when logged in
        url(r'^profile/', regviews.profile, name="profile"),

        #Update your profile information
        url(r'^profile/update/', regviews.profileUpdate, name='profileUpdate'),


        #REGISTRATION VIEWS
        #---------

        #Register
        url(r'^signup/', regviews.index, name='signup'),

        #Login
        url(r'^signin/', regviews.signin, name = 'signin'),

        #Logout
        url(r'^signout/', regviews.signout, name='signout'),

        #Display password options
        url(r'^password/', regviews.passwordMenu, name = 'passwordMenu'),

        #Change password
        url(r'^password/change/', regviews.passwordChange, name = 'passwordChange'),
        
        #Reset password
        url(r'^password/reset/', regviews.passwordReset, name= 'passwordReset'),

)
