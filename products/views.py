from django.views.generic import DetailView, ListView

from .models import Product


class ProductDetailView(DetailView):
    queryset = Product.available.all()


class ProductListView(ListView):
    paginate_by = 6

    def get_queryset(self):
        queryset = Product.available.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
