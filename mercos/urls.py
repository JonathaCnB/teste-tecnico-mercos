from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Direcionamento para pagina principal
    path("", include("pages.urls")),
    # Direcionamento para pagina produtos
    path("products/", include("products.urls")),
    # Direcionamento para pagina pedidos
    path("order/", include("order.urls")),
]

#  configuração para servir os arquivos de midia localmente
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
