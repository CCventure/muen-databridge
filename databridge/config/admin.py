from django.contrib import admin
from .models import CityConfiguration, PriceConfiguration, StockConfiguration

@admin.register(CityConfiguration)
class CityConfigurationAdmin(admin.ModelAdmin):
    list_display = ('get_city_id_display', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('city_id',)
    ordering = ('city_id',)
    
    def has_add_permission(self, request):
        # Only allow one instance per city
        return CityConfiguration.objects.count() < len(CityConfiguration.CITY_CHOICES)
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of active configurations
        if obj and obj.is_active:
            return False
        return super().has_delete_permission(request, obj)


@admin.register(PriceConfiguration)
class PriceConfigurationAdmin(admin.ModelAdmin):
    list_display = ('PRICE_THRESHOLD', 'BELOW_THRESHOLD_MULTIPLIER', 'ABOVE_THRESHOLD_MULTIPLIER', 
                    'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    
    def has_add_permission(self, request):
        # Only allow one active configuration
        active_configs = PriceConfiguration.objects.filter(is_active=True).count()
        return active_configs < 1
    
    def save_model(self, request, obj, form, change):
        # Ensure only one active configuration at a time
        if obj.is_active:
            PriceConfiguration.objects.exclude(pk=obj.pk).update(is_active=False)
        super().save_model(request, obj, form, change)


@admin.register(StockConfiguration)
class StockConfigurationAdmin(admin.ModelAdmin):
    list_display = ('is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    
    def has_add_permission(self, request):
        # Only allow one active configuration
        active_configs = StockConfiguration.objects.filter(is_active=True).count()
        return active_configs < 1
    
    def save_model(self, request, obj, form, change):
        # Ensure only one active configuration at a time
        if obj.is_active:
            StockConfiguration.objects.exclude(pk=obj.pk).update(is_active=False)
        super().save_model(request, obj, form, change)

