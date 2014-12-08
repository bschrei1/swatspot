from django.conf.urls import patterns, include, url
from django.contrib import admin
from sharples import views


urlpatterns = patterns('',
    url(r'^sharples/', include('sharples.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^students/', views.students, name='students'),
    url(r'^closing/',views.closing, name='closing'),
    url(r'^opening/',views.opening, name='opening'),

    url(r'^$', views.students, name='students')
   # url(r'^students/', include('sharples.urls')),# why doesnt this work??
)
"""
urlpatterns = patterns('',
    url(r'^students/', include('sharples.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
"""
