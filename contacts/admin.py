from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'request', 'email', 'phone', 'contact_date')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email', 'phone', 'request')
    list_per_page = 25


admin.site.register(Contact, ContactAdmin)
