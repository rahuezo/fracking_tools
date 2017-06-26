from django.conf.urls import url

from . import views

app_name = 'pairwise_comparisons'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'multi_file_upload/$', views.multi_file_upload, name='multi_file_upload'),
    url(r'multi_file_upload_success/$', views.multi_file_upload_success, name='multi_file_upload_success'),
    url(r'spreadsheet_upload/$', views.spreadsheet_upload, name='spreadsheet_upload'),
    url(r'download_comparison_summary/$', views.download_comparison_summary, name='download_comparison_summary'),
    url(r'generate_comparison_summary/$', views.generate_comparison_summary, name='generate_comparison_summary'),
]