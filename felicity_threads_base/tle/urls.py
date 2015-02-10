from django.conf.urls import patterns, url

from django.conf import settings
from django.conf.urls.static import static
from tle import views

urlpatterns = patterns('',
    url(r'^$' , views.index, name='index'),
    url(r'^problems$', views.problems, name='problems'),
    url(r'^question/(\d{1,2})/(\d{1,2})$', views.question, name='question'),
    url(r'^submit/(\d{1,2})/(\d{1,2})$', views.submit, name='submit'),
    url(r'^comment_submit/(\d{1,2})/(\d{1,2})$', views.comment_submit, name='comment_submit'),
    url(r'^scoreboard$', views.scoreboard, name='scoreboard'),
)
#regex \d{1,2} means that the question level or question id will be at max 99.