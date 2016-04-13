from django.conf.urls import patterns
from django.conf.urls import url

from myplugin.content.mypanel import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
)
