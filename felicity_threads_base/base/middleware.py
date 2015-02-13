from django.http import HttpResponseForbidden, HttpResponseRedirect 
from django.conf import settings
from django.contrib.auth.views import login, logout
from django_cas.views import login as cas_login, logout as cas_logout
import datetime
from base.models import User
from django.shortcuts import render

class UTC(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(0)
    def tzname(self, dt):
        return "UTC"
    def dst(self, dt):
        return datetime.timedelta(0)

utc = UTC()

class RestrictAccessTillTime(object):

    def process_request(self, request):
        pass

    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func == login or view_func == logout or view_func == cas_login or view_func == cas_logout:
            return None
        time_now = datetime.datetime.now(utc)
        if request.user.is_authenticated():
            if request.user.is_staff:
                return None
            profile = User.objects.filter(user_username=request.user.username)[0]
            user_nick = profile.user_nick
            if time_now < settings.CONTEST_START_DATETIME or time_now > settings.CONTEST_END_DATETIME:
                return render(request, 'base/error.html', {'error_code': 6, 'user_nick':user_nick} , status = 401)
            else:
                return None
        else:
            if time_now < settings.CONTEST_START_DATETIME or time_now > settings.CONTEST_END_DATETIME:
                return render(request, 'base/error.html', {'error_code': 6, 'user_nick': None} , status = 401 )
            else:
                return None
