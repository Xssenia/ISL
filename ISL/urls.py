from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('books/', include('books.urls')),
    path('loans/', include('loans.urls')),
    path('admin_panel/', include('admin_panel.urls')),
    path('backups/', include('backups.urls')),
    path('', include('books.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
