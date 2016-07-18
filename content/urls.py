from django.conf.urls import url
from django.contrib import admin
from .views import *


urlpatterns = [
    url(r'^(?P<a_id>\d+)/$', detail_art_view, name='detail_view'),
    url(r'^add/$', add_post, name='add_view'),
    url(r'^(?P<a_id>\d+)/del', del_post, name='del_view'),
    url(r'^(?P<a_id>\d+)/like', like_post, name='like_view'),

]
