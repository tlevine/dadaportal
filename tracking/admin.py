from django.contrib import admin

from .models import Hit

class HitAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'datetime_start', 'session', 'ip_address',
                    'referrer', 'status_code', 'javascript_enabled', )
    list_filter = ('status_code', 'javascript_enabled', 'endpoint')
    date_hierarchy = 'datetime_start'
    ordering = ('-datetime_start',)

admin.site.register(Hit, HitAdmin)
