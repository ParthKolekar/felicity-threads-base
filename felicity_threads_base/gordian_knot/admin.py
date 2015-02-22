from django.contrib import admin

from gordian_knot.models import *

# Register your models here.
admin.site.register(Question)
admin.site.register(Submission)
admin.site.register(Comment)
