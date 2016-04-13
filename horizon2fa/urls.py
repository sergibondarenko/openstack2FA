from django.conf.urls import patterns
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index$', views.index, name='index'),
    url(r'^loginview$', views.loginview, name='loginview'),
    url(r'^login$', views.login, name='login'),
    url(r'^newview$', views.newview, name='newview'),
    url(r'^new$', views.new, name='new'),
    url(r'^code$', views.code, name='code'),
    url(r'^qr.*', views.qr, name='qr'),
    url(r'^otpconfirm$', views.otpconfirm, name='otpconfirm'),
]

