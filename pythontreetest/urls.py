from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from bigtree import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tree.views.home', name='home'),
    # url(r'^tree/', include('tree.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^catalog/', include('bigtree.urls')),
)
