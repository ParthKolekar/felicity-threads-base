from django.conf.urls import patterns, url

from django.conf import settings
from django.conf.urls.static import static
from base import views

urlpatterns = patterns('',
	url(r'^$' , views.index, name='index'),
    url(r'^problems$', views.problems, name='problems'),
    url(r'^question/(\d{1,2})/(\d{1,2})$', views.question, name='question'),
)
