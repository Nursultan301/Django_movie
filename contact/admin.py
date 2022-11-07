from django.contrib import admin

from contact.models import Contact


@admin.register(Contact)
class AdminContact(admin.ModelAdmin):
    list_display = ("email", "date")
