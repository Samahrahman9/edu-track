from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.conf.urls import handler404

handler404 = 'core.views.handler404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('reporting/', include('reporting.urls')),
    path('accounts/', include('accounts.urls')),  # uses your custom login/logout/signup
]
