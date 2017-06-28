from django.conf.urls import url

from . import views

app_name = 'pairwise_comparisons'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'download_comparison_summary/$', views.download_comparison_summary, name='download_comparison_summary'),
    url(r'generate_comparison_summary/$', views.generate_comparison_summary, name='generate_comparison_summary'),
    url(r'file_upload/$', views.index, name='file_upload'),
    # url(r'view_comparison_summary/$', views.view_comparison_summary, name='view_comparison_summary'),
]