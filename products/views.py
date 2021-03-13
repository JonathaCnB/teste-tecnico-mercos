from django.views.generic import DetailView, ListView
from order.forms import OrderAddProductsForm

from .models import Product


class ProductDetailView(DetailView):
    queryset = Product.available.all()
    extra_context = {"form": OrderAddProductsForm()}


class ProductListView(ListView):
    paginate_by = 6

    def get_queryset(self):
        queryset = Product.available.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
