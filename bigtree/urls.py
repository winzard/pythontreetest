__author__ = 'winzard'
from django.conf.urls import patterns, include, url
from bigtree import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'^generate/$', views.generate, name='generate'),
    url(r'^display/$', views.display, name='display'),
    url(r'^manage/(\d*)$', views.manage, name='manage'),
)
