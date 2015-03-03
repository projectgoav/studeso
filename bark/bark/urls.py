from django.conf.urls import patterns, include, url
from django.contrib import admin

from bark.views import views, regviews

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bark.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),


		#Main Application URLs
        url(r'^$', views.index, name='index'),

        #Registration Views
        url(r'signup/', regviews.index, name='regIndex')

)
