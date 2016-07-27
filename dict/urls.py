from .views import write_text, show_texts, solution
from django.conf.urls import url


urlpatterns = [
    url(r'^$', show_texts),
    url(r'^(?P<text_id>\d+)/$', write_text, name='write_view'),

]
