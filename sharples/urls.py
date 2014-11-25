from django.conf.urls import patterns, url

from sharples import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    
    url(r'students/$', views.students, name='students'),
    url(r'^(?P<update_id>\d+)/$', views.detail, name='detail'),
    )
    #replacing the class question with the update class 

