from django.contrib import admin
from .models import Division, Executive, Gadget, Villain, CloudKPI

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name','focus','cloud_priority','order')
    list_filter  = ('cloud_priority',)

@admin.register(Executive)
class ExecutiveAdmin(admin.ModelAdmin):
    list_display = ('role','name','level','is_active','order')
    list_filter  = ('level','is_active')

@admin.register(Gadget)
class GadgetAdmin(admin.ModelAdmin):
    list_display = ('code','name','classification','status','year_developed','threat_neutralized')
    list_filter  = ('classification','status')
    search_fields = ('name','code')

@admin.register(Villain)
class VillainAdmin(admin.ModelAdmin):
    list_display = ('alias','name','threat_level','status','times_detained')
    list_filter  = ('threat_level','status')

@admin.register(CloudKPI)
class CloudKPIAdmin(admin.ModelAdmin):
    list_display = ('pillar','metric_name','target','current','progress','trend_up')
    list_filter  = ('pillar','trend_up')
