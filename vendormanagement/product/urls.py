from django.urls import path

from vendormanagement.product.api.v1 import views

urlpatterns = [
    path("products/", views.ProductViewsets.as_view({"get": "list"})),
    path("outlets/", views.OutletViewsets.as_view({"get": "list"})),
    path("outlet-create/", views.OutletViewsets.as_view({"post": "create"})),
    path(
        "product-create/<uuid:outlet_uuid>",
        views.ProductViewsets.as_view({"post": "create"}),
    ),
    path(
        "product-update/<uuid:product_uuid>",
        views.ProductViewsets.as_view({"patch": "patch"}),
    ),
]
