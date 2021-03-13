import pytest
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from products.tests.factories import ProductFactory

from ..order import Order

pytestmark = pytest.mark.django_db


def dummy_get_response(request):
    return None


@pytest.fixture
def http_request():
    request = HttpRequest()
    middleware = SessionMiddleware(dummy_get_response)
    middleware.process_request(request)
    return request


@pytest.fixture
def session(http_request):
    return http_request.session


@pytest.fixture
def order(http_request, session):
    order = Order(http_request)
    session.modified = False
    return order


def test_create_empty_order(http_request, session):
    assert session.get("order") is None
    Order(http_request)
    assert session["order"] == {}


def test_get_non_empty_order(http_request, session):
    session["order"] = {"1": {}}
    Order(http_request)
    assert session["order"] == {"1": {}}


def test_add_product_to_empty_order(product, order, session):
    order.add(product)

    assert session["order"] == {
        str(product.id): {"quantity": 1, "price": str(product.price)}
    }
    assert session.modified


def test_add_product_to_empty_order_quantity_gt_1(product, order, session):
    order.add(product, 2)

    assert session["order"] == {
        str(product.id): {"quantity": 2, "price": str(product.price)}
    }
    assert session.modified


def test_add_product_to_empty_cart_twice(product, order, session):
    order.add(product)
    session.modified = False

    order.add(product, 2)

    assert session["order"] == {
        str(product.id): {"quantity": 3, "price": str(product.price)}
    }
    assert session.modified


def test_add_product_to_empty_override_quantity(product, order, session):
    order.add(product)
    session.modified = False

    order.add(product, 4, override_quantity=True)

    assert session["order"] == {
        str(product.id): {"quantity": 4, "price": str(product.price)}
    }
    assert session.modified


def test_remove_product(product, order, session):
    order.add(product)
    session.modified = False

    order.remove(product)
    assert session["order"] == {}
    assert session.modified


def test_remove_product_not_in_order(product, order, session):
    order.remove(product)
    assert session["order"] == {}
    assert not session.modified


def test_cart_iter(order, session):
    p1 = ProductFactory()
    p2 = ProductFactory()
    p3 = ProductFactory()

    order.add(p1)
    order.add(p2, 2)
    order.add(p3, 3)
    session.modified = False

    products = [p1, p2, p3]
    quantities = [1, 2, 3]

    for product, quantity, item in zip(products, quantities, order):
        assert product.price == item["price"]
        assert product.price * quantity == item["total_price"]
        assert product == item["product"]
        assert "update_quantity_form" in item

    assert not session.modified
    assert list(order.order.values()) != list(iter(order))


def test_order_length(order):
    p1 = ProductFactory()
    p2 = ProductFactory()

    assert len(order) == 0

    order.add(p1)
    assert len(order) == 1

    order.add(p2, 3)
    assert len(order) == 4


def test_get_total_price(order):
    p1 = ProductFactory()
    p2 = ProductFactory()

    order.add(p1)
    order.add(p2, 2)

    total_price = p1.price + (p2.price * 2)

    assert order.get_total_price() == total_price
