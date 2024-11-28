from django.contrib import admin
from .models import AdminActionLog

@admin.register(AdminActionLog)
class AdminActionLogAdmin(admin.ModelAdmin):
    list_display = ('admin_user', 'book', 'action', 'reason', 'created_at')
    list_filter = ('action', 'admin_user', 'created_at')
    search_fields = ('book__title', 'admin_user__username', 'reason')
