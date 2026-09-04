from django.contrib import admin
from .models import Client, PolicyType, Policy


admin.site.register(Client)
admin.site.register(PolicyType)
admin.site.register(Policy)
