from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^storage/$', views.storage, name='storage'),
    url(r'^statistic/$', views.statistic, name='statistic'),
]