from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'felicity_threads_base.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^contest/admin/', include(admin.site.urls)),
    #url(r'^base/' , include('base.urls')),
    url(r'^contest/accounts/login' , 'django_cas.views.login'),
    url(r'^contest/accounts/logout' ,'django_cas.views.logout'),
    url(r'^contest/break_in/' , include('tle.urls')), 
) + static (settings.STATIC_URL , document_root = settings.STATIC_ROOT) + static (settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)

