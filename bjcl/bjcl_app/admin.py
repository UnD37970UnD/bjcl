from django.contrib import admin

from .models import result
from .models import searchers

admin.site.register(result)
admin.site.register(searchers)