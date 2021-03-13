from django.urls import path

from .views import order_add, order_detail, order_remove

app_name = "order"

urlpatterns = [
    path("", order_detail, name="detail"),
    path("add/<int:product_id>/", order_add, name="add"),
    path("remove/<int:product_id>/", order_remove, name="remove"),
]
