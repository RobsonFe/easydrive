from django.urls import include, path

urlpatterns = [
    path('', include('api.accounts.urls')),
    path('', include('api.auth.urls')),
    path('', include('api.client.urls')),
    path('', include('api.vehicle.urls')),
    path('', include('api.rent.urls')),
]

