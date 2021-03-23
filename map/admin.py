from django.contrib import admin
from .models import Map, LogisticsNetwork, Cities, HistoryLogisticNetwork

class LogisticsNetworkInline(admin.TabularInline):
    model = LogisticsNetwork
    extra = 0
    min_num = 1

class MapAdmin(admin.ModelAdmin):
    model = Map
    inlines = [LogisticsNetworkInline]
    list_display = ['name']
    search_fields = ['name']
    ordering = ['id']

admin.site.register(Map, MapAdmin)
admin.site.register(LogisticsNetwork)
admin.site.register(Cities)
admin.site.register(HistoryLogisticNetwork)
