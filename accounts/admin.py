from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'send_updates', 'update_frequency']
    list_display_links = ['user']
    list_filter = ['user', 'send_updates', 'update_frequency']
    list_editable = ['send_updates']
    search_fields = ['user', 'update_frequency']
    list_per_page = 25
