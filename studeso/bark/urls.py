from django.conf.urls import patterns, url
from bark import views, regviews

#Our Bark Application Urls
urlpatterns = patterns('',

		#Main Application URLs
        url(r'^$', views.index, name='index'),

        #Registration Views
        url(r'signup/', regviews.index, name='regIndex'),

        )