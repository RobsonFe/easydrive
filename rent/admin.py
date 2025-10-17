from django.contrib import admin
from rent.models import Rental


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'vehicle', 'start_date', 'end_date', 'returned')
    list_filter = ('returned', 'start_date', 'end_date')
    search_fields = ('client__user__username', 'client__user__name', 'vehicle__brand', 'vehicle__model')
    readonly_fields = ('id',)
    
    fieldsets = (
        ('Informações do Aluguel', {
            'fields': ('client', 'vehicle', 'start_date', 'end_date', 'returned')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('client__user', 'vehicle')