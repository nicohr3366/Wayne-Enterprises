from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('ventures/', include('apps.ventures.urls')),
    path('foundation/', include('apps.foundation.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('realestate/', include('apps.realestate.urls')),
    path('capital/', include('apps.capital.urls')),
    path('industries/', include('apps.industries.urls')),
    path('healthcare/', include('apps.healthcare.urls')),
    path('tech/', include('apps.tech.urls')),
]
