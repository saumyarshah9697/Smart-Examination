from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Qbank)
admin.site.register(Test)
admin.site.register(Score)
admin.site.register(TestLog)

