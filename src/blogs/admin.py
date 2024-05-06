from django.contrib import admin
from .models import AppUser, LogEntry

admin.site.register(AppUser)
admin.site.register(LogEntry)
