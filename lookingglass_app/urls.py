# Seperate URL file for searchApp application,
# keeps main urls.py clean

from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    # url(r'^$', views.search_page, name='home'),
    url(r'^$', views.search_page, name='search'),
    url(r'display_images/(\d+)/$', views.display_images, name='images'),
]

urlpatterns += staticfiles_urlpatterns()
