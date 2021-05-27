from django.contrib import admin
from .models import Request, Response


class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude', 'check_weekly', 'user', 'date_uploaded', 'response')
    list_display_links = ('id', )
    list_editable = ('check_weekly',)
    search_fields = ('latitude', 'longitude', 'user')
    list_per_page = 30


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'date_uploaded')
    list_display_links = ('id', '__str__')
    list_per_page = 30


admin.site.register(Request, RequestAdmin)
admin.site.register(Response, ResponseAdmin)
