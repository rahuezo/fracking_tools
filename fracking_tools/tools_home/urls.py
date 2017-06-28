from django.conf.urls import url

from . import views

app_name = 'tools_home'

urlpatterns = [
    url(r'^$', views.index, name='index'),
]