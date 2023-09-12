from django.contrib import admin

from .models import User, UserTasks

admin.site.register(User)
admin.site.register(UserTasks)
