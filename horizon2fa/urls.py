from django.conf.urls import patterns
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^code$', views.code, name='code'),
    url(r'^new$', views.new, name='new'),
    url(r'^qr.*', views.qr, name='qr'),
    url(r'^otpconfirm$', views.otpconfirm, name='otpconfirm'),
]
