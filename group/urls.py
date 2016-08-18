from .views import groups, create_group, group, new_topic, topic, members, del_group, invite_to_group, join_to_group
from .views import leave_group
from django.conf.urls import url


urlpatterns = [
    url(r'^$', groups),
    url(r'create$', create_group),
    url(r'^(?P<g_id>\d+)/$', group, name='group'),
    url(r'^(?P<g_id>\d+)/new_topic/$', new_topic),
    url(r'^(?P<g_id>\d+)/members/$', members),
    url(r'^(?P<g_id>\d+)/delete/$', del_group, name='del_group'),
    url(r'^(?P<g_id>\d+)/invite/$', invite_to_group, name='invite'),
    url(r'^(?P<g_id>\d+)/leave/$', leave_group, name='leave_group'),
    url(r'^(?P<g_id>\d+)/join/(?P<token>[-\w]+)/$', join_to_group, name='join_to_group'),
    url(r'^(?P<g_id>\d+)/(?P<slug>[-\w]+)/$', topic),

]
