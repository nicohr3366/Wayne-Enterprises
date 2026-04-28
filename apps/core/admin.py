from django.contrib import admin
from .models import DefenseContract


@admin.register(DefenseContract)
class DefenseContractAdmin(admin.ModelAdmin):
    list_display = ('contract_number', 'agency', 'contractor_name', 'obligated_amount_usd', 'fiscal_year', 'performance_status', 'etl_source_system')
    list_filter = ('agency', 'fiscal_year', 'performance_status', 'security_classification', 'cyber_compliance_level', 'small_business', 'veteran_owned')
    search_fields = ('contract_number', 'contractor_name', 'contract_id', 'agency')
    ordering = ('-obligated_amount_usd',)
    readonly_fields = ('created_at',)
