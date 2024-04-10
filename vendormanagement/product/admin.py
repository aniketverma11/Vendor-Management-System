from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Outlet


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "name",
        "type",
        "manufacturer",
        "outlet",
        "get_vendor_name",
        "price",
        "productUnit",
        "productSoldUnit",
    ]
    search_fields = ["name", "manufacturer"]
    list_filter = ["type"]
    ordering = ["name"]

    def get_vendor_name(self, obj):
        return obj.vendor.name if obj.vendor else None

    get_vendor_name.short_description = "Vendor Name"


@admin.register(Outlet)
class OutletAdmin(admin.ModelAdmin):
    list_display = ["uuid", "name", "location", "get_vendor_name"]
    search_fields = ["name", "location"]
    ordering = ["name"]

    def get_vendor_name(self, obj):
        return obj.vendor.name if obj.vendor else None

    get_vendor_name.short_description = "Vendor Name"
