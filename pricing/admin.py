from django.contrib import admin
from .models import PricingConfig, PricingConfigLog
from .forms import PricingConfigForm

@admin.register(PricingConfig)
class PricingConfigAdmin(admin.ModelAdmin):
    form = PricingConfigForm
    list_display = ('day_of_week', 'distance_base_price', 'is_active', 'updated_at')
    list_filter = ('day_of_week', 'is_active')
    search_fields = ('day_of_week',)

@admin.register(PricingConfigLog)
class PricingConfigLogAdmin(admin.ModelAdmin):
    list_display = ('config', 'actor', 'action', 'timestamp')
    search_fields = ('actor__username', 'action')
    readonly_fields = ('config', 'actor', 'action', 'timestamp')
