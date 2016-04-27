from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.search_page, name='search'),
    url(r'^display_images/', views.display_images, name='images'),
    url(r'^extension/', views.extract_text, name='chrome'),
    url(r'^test/', views.test, name='chrome'),
    url(r'^reco/', views.reco, name='chrome'),
]