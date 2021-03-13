import copy
from decimal import Decimal

from products.models import Product

from .forms import OrderAddProductsForm


class Order:
    def __init__(self, request):
        if request.session.get("order") is None:
            request.session["order"] = {}

        self.order = request.session["order"]
        self.session = request.session

    def __iter__(self):
        order = copy.deepcopy(self.order)

        products = Product.objects.filter(id__in=order)
        for product in products:
            order[str(product.id)]["product"] = product

        for item in order.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            item["update_quantity_form"] = OrderAddProductsForm(
                initial={"quantity": item["quantity"], "override": True}
            )
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.order.values())

    def add(self, product, quatity=1, override_quantity=False):
        product_id = str(product.id)

        if product_id not in self.order:
            self.order[product_id] = {
                "quantity": 0,
                "price": str(product.price),
            }

        if override_quantity:
            self.order[product_id]["quantity"] = quatity
        else:
            self.order[product_id]["quantity"] += quatity

        self.save()

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.order:
            del self.order[str(product.id)]
            self.save()

    def get_total_price(self):
        return sum(
            item["quantity"] * Decimal(item["price"])
            for item in self.order.values()
        )

    def save(self):
        self.session.modified = True
