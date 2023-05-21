from django.contrib import admin

# Register your models here.

from .models import PacketType, Protocol


class ReceiverModeAdmin(admin.ModelAdmin):
    fields = ["mode", "enabled"]


admin.site.register(PacketType)
admin.site.register(Protocol, ReceiverModeAdmin)
