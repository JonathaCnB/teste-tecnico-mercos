from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse


#  Metodo para fildro direto dos produtos que estão disponiveis
class AvailableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_available=True)


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(unique=True, always_update=False, populate_from="name")
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=50, decimal_places=2)
    is_available = models.BooleanField(default=True)

    objects = models.Manager()
    available = AvailableManager()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})
