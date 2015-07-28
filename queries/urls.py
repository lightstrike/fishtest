from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.fish_queries, name='fish_queries'),
]