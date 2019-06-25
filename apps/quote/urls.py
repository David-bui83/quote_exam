from django.conf.urls import url
from . import views 

urlpatterns = [
  url(r'^$', views.index),
  url(r'^registor$', views.registor),
  url(r'^login$', views.login),
  url(r'^quotes$', views.quotes),
  url(r'create$', views.create_quote),
  url(r'^users/(?P<id>\d+)$', views.users_view),
  url(r'^add/(?P<id>\d+)$', views.add),
  url(r'^remove/(?P<id>\d+)$', views.remove),
  url(r'^logout$', views.logout)
]