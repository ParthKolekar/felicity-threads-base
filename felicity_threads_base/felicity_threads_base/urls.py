from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'felicity_threads_base.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^base/' , include('base.urls')),
    url(r'^accounts/login' , 'django_cas.views.login'),
    url(r'^accounts/logout' ,'django_cas.views.logout'),
    url(r'^cache_in/' , include('cache_in.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )