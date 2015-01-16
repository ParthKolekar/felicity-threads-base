from django.http import HttpResponseForbidden
from django.conf import settings
import datetime

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
        if request.user.is_authenticated():
            time_now = datetime.datetime.now(utc)
            if time_now > settings.CONTEST_START_DATETIME and time_now < settings.CONTEST_END_DATETIME:
                return None
            else:
                if request.user.is_staff:
                    return None
                else:
                    error = ('<h1>Forbidden</h1><p>Contest Not Started</p>')
                    return HttpResponseForbidden(error)
        else:
            return None
