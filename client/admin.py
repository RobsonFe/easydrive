from django.contrib import admin
from client.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_rentals')
    list_filter = ('total_rentals',)
    search_fields = ('user__username', 'user__name', 'user__email')
    readonly_fields = ('total_rentals',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')