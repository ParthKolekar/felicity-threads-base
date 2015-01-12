from django.conf.urls import patterns, url

from django.conf import settings
from django.conf.urls.static import static
from cache_in import views

urlpatterns = patterns('',
	url(r'^$' , views.index, name='index'),
    url(r'^problems$', views.problems, name='problems'),
    #url(r'^submissions$', views.submissions, name='submissions'),

    #regex \d{1,2} means that the question level or question id will be at max 99.
    url(r'^question/(\d{1,2})/(\d{1,2})$', views.question, name='question'),
    url(r'^submit/(\d{1,2})/(\d{1,2})$', views.submit, name='submit'),
)
