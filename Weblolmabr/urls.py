"""Weblolmabr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from content.views import about_page, IndexPage, LoginFormView, log_out, contact_page, thanks_page
from dict.views import solution, solutions
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'^$', IndexPage.as_view(), name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^post/', include('content.urls')),
    url(r'^text/', include('dict.urls')),
    url(r'^groups/', include('group.urls')),
    url(r'^about/$', about_page, name='about'),
    url(r'^logout/$', log_out, name='logout'),
    url(r'^login/$', LoginFormView.as_view(), name='login'),
    url(r'^contact/$', contact_page, name='contact_page'),
    url(r'^thanks/$', thanks_page),
    url(r'^solution/(?P<id>\d+)/$', solution, name='solution_view'),
    url(r'^solutions/$', solutions),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
