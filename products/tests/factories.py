import factory
import factory.fuzzy

from ..models import Product


class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    image = factory.django.ImageField()
    description = factory.Faker(
        "paragraph",
        nb_sentences=3,
        variable_nb_sentences=True,
    )
    price = factory.fuzzy.FuzzyDecimal(1000.00, 5000000.00)
    is_available = factory.Faker("pybool")

    class Meta:
        model = Product
