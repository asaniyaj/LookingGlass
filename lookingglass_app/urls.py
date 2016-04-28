from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.search_page, name='search'),
    url(r'^extension/', views.extract_text, name='chrome'),
    url(r'^test/', views.test, name='chrome'),
    url(r'^reco/', views.reco, name='chrome'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),

]