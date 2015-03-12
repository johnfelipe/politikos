from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views

urlpatterns = patterns('',
    url(r'^$', views.RepresentativesSearchView.as_view(), name='search-representatives'),
    url(r'^person/(?P<id>\w+)/$', views.PersonDetail.as_view(), name='person-detail'),
    url(r'^istitution/(?P<id>\w+)/$', views.InstitutionDetail.as_view(), name='institution-detail'),

    # url(r'^admin/', include(admin.site.urls)),
)
