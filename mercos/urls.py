from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Direcionamento para pagina principal
    path("", include("pages.urls")),
]
