from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from utils.behaviours import (
    UUIDMixin,
    MobileMixin,
    ImageMixin,
    UserStampedMixin,
    StatusMixin,
    EmailMixin,
)
from vendormanagement.users.models import Vendor


class Outlet(UUIDMixin, EmailMixin, MobileMixin, StatusMixin, UserStampedMixin):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    productUnit = models.PositiveIntegerField(default=0)
    name = models.CharField(_("Name of Outlet"), blank=True, max_length=255)
    location = models.CharField(_("Outlet Location"), blank=True, max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Outlet"
        verbose_name_plural = "Outlet"


class Product(UUIDMixin, StatusMixin, UserStampedMixin):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, null=True, blank=True)
    productUnit = models.PositiveIntegerField(default=0)
    productSoldUnit = models.PositiveIntegerField(default=0)
    name = models.CharField(_("Name of Product"), blank=True, max_length=255)
    type = models.CharField(_("Type"), blank=True, max_length=255)
    manufacturer = models.CharField(_("Manufacturer"), blank=True, max_length=255)
    price = models.CharField(_("Price"), blank=True, max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Product"
