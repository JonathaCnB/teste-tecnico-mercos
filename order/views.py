from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from products.models import Product

from .forms import OrderAddProductsForm
from .order import Order


def order_detail(request):
    order = Order(request)
    return render(request, "order/order_detail.html", {"order": order})


@require_POST
def order_add(request, product_id):
    order = Order(request)
    product = get_object_or_404(Product, id=product_id)

    form = OrderAddProductsForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        order.add(
            product=product,
            quatity=cd["quantity"],
            override_quantity=cd["override"],
        )

    return redirect("order:detail")


@require_POST
def order_remove(request, product_id):
    order = Order(request)
    product = get_object_or_404(Product, id=product_id)
    order.remove(product)
    return redirect("order:detail")
