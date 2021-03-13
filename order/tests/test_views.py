import pytest
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


class TestOrderAddView:
    def test_reverse_resolve(self, product):
        assert (
            reverse("order:add", kwargs={"product_id": product.id})
            == f"/order/add/{product.id}/"
        )
        assert resolve(f"/order/add/{product.id}/").view_name == "order:add"

    def test_add_product_to_order(self, client, product):
        response = client.post(
            reverse("order:add", kwargs={"product_id": product.id}),
            data={"quantity": 1, "override": False},
        )
        assert response.status_code == 302
        assert response.url == "/order/"
        assert str(product.id) in client.session["order"]


class TestOrderRemoveView:
    def test_reverse_resolve(self, product):
        assert (
            reverse("order:remove", kwargs={"product_id": product.id})
            == f"/order/remove/{product.id}/"
        )
        assert (
            resolve(f"/order/remove/{product.id}/").view_name == "order:remove"
        )

    def test_remove_product_to_order(self, client, product):
        response = client.post(
            reverse("order:remove", kwargs={"product_id": product.id}),
            data={"quantity": 1, "override": False},
        )
        assert response.status_code == 302
        assert response.url == "/order/"
        assert str(product.id) not in client.session["order"]


class TesteOrderDetailView:
    def test_reverse_resolve(self, product):
        assert reverse("order:detail") == "/order/"
        assert resolve("/order/").view_name == "order:detail"

    def test_status_code(self, client):
        response = client.get(reverse("order:detail"))
        assert response.status_code == 200
