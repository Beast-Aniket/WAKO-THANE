from django.contrib import admin
from .models import SiteSettings, ContactMessage

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_read')
    list_filter = ('is_read',)
