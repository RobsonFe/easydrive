from django.contrib import admin
from vehicle.models import Vehicle, TypeVehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'model', 'year', 'type_vehicle', 'quantity', 'is_available')
    list_filter = ('type_vehicle', 'is_available', 'year')
    search_fields = ('brand', 'model', 'description')
    readonly_fields = ('is_available',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('brand', 'model', 'year', 'type_vehicle')
        }),
        ('Estoque', {
            'fields': ('quantity', 'is_available')
        }),
        ('Descrição', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
    )