"""
URL configuration for leads_manager project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'ok', 'message': 'Server is running'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('health', health_check, name='health'),
]

