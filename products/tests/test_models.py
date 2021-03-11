import pytest
from pytest_django.asserts import assertQuerysetEqual

from ..models import Product
from .factories import ProductFactory

pytestmark = pytest.mark.django_db


class TestProductModel:
    def test__str__(self, product):
        assert product.__str__() == product.name
        assert str(product) == product.name

    def test_get_absolute_url(self, product):
        url = product.get_absolute_url()
        assert url == f"/products/{product.slug}/"

    def test_available_manager(self):
        ProductFactory(is_available=True)
        ProductFactory(is_available=False)

        assert Product.objects.all().count() == 2
        assert Product.available.all().count() == 1
        assertQuerysetEqual(
            Product.available.all(),
            Product.objects.filter(is_available=True),
            transform=lambda x: x,
        )
