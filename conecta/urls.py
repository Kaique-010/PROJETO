from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from produtos.admin import custom_admin_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('custom_admin/', custom_admin_site.urls),
    path('', include('core.urls')),
    path('produtos/', include('produtos.urls')),
    path('carrinho/', include('carrinho.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
