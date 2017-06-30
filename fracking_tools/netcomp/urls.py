from django.conf.urls import url

from . import views

app_name = 'netcomp'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'build_networks_from_events/$', views.build_networks_from_events, name='build_networks_from_events'),
    url(r'build_networks_from_pairs/$', views.build_networks_from_pairs, name='build_networks_from_pairs'),
    url(r'file_upload/$', views.build_networks_from_events, name='file_upload'),
    url(r'download_events_zip/$', views.download_events_zip, name='download_events_zip'),
]