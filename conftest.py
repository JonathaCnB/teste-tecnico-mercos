import pytest

from products.tests.factories import ProductFactory


# fixture para criação de uma pasta temporaria para imagens
@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def product():
    return ProductFactory()
