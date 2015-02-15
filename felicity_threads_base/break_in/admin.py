from django.contrib import admin
from break_in.models import *

# Register your models here.
admin.site.register(Question)
admin.site.register(Submission)
admin.site.register(Comment)
admin.site.register(Team)
admin.site.register(TeamUser)
