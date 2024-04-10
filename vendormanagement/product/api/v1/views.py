from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from vendormanagement.product.models import Outlet, Product

from utils.response import cached_response

from .serializers import (
    ProductSerializer,
    OutletSerializer,
    ProductUnitUpdateSerializer,
)


class ProductViewsets(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True, is_deleted=False)

    def list(self, request):
        user = request.user
        vendor = user.vendor

        products = self.queryset.filter(vendor__uuid=vendor.uuid)
        serializer = self.serializer_class(products, many=True).data
        return cached_response(
            request=request,
            status=status.HTTP_200_OK,
            response_status="success",
            message="",
            data=serializer,
            meta={},
        )

    def create(self, request, outlet_uuid):
        # Check if user has permission to add product
        if not (
            request.user.has_perm("product.add_product")
            and request.user.role == "supervisor"
        ):
            return cached_response(
                request=request,
                status=status.HTTP_403_FORBIDDEN,
                response_status="failed",
                message="You don't have permission to add an Product",
                data={},
                meta={},
            )

        data = request.data.copy()
        data["outlet"] = str(outlet_uuid)

        serializer = ProductSerializer(data=data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return cached_response(
                request=request,
                status=status.HTTP_201_CREATED,
                response_status="success",
                message="",
                data=serializer.data,
                meta={},
            )
        return cached_response(
            request=request,
            status=status.HTTP_400_BAD_REQUEST,
            response_status="failed",
            message="",
            data=serializer.errors,
            meta={},
        )

    def patch(self, request, product_uuid):
        # Check if user has permission to add product
        if not (
            request.user.has_perm("product.change_product")
            and request.user.role == "salesperson"
        ):
            return cached_response(
                request=request,
                status=status.HTTP_403_FORBIDDEN,
                response_status="failed",
                message="You don't have permission to update an product",
                data={},
                meta={},
            )

        data = request.data.copy()
        data["product"] = str(product_uuid)

        serializer = ProductUnitUpdateSerializer(
            data=data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            try:
                product = Product.objects.get(uuid=product_uuid)
            except Product.DoesNotExist:
                return cached_response(
                    request=request,
                    status=status.HTTP_404_NOT_FOUND,
                    response_status="failed",
                    message="Product not found",
                    data={},
                    meta={},
                )

            serializer.update(product, serializer.validated_data)
            return cached_response(
                request=request,
                status=status.HTTP_205_RESET_CONTENT,
                response_status="success",
                message="",
                data=serializer.data,
                meta={},
            )
        return cached_response(
            request=request,
            status=status.HTTP_400_BAD_REQUEST,
            response_status="failed",
            message="",
            data=serializer.errors,
            meta={},
        )


class OutletViewsets(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = OutletSerializer
    queryset = Outlet.objects.filter(is_active=True, is_deleted=False)

    def list(self, request):
        user = request.user
        vendor = user.vendor

        outlets = self.queryset.filter(vendor__uuid=vendor.uuid)
        serializer = self.serializer_class(outlets, many=True).data
        return cached_response(
            request=request,
            status=status.HTTP_200_OK,
            response_status="success",
            message="",
            data=serializer,
            meta={},
        )

    def create(self, request):
        # Check if user has permission to add outlet
        if not (
            request.user.has_perm("product.add_outlet") and request.user.role == "admin"
        ):
            return cached_response(
                request=request,
                status=status.HTTP_403_FORBIDDEN,
                response_status="failed",
                message="You don't have permission to add an outlet",
                data={},
                meta={},
            )

        data = request.data.copy()

        serializer = OutletSerializer(data=data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return cached_response(
                request=request,
                status=status.HTTP_201_CREATED,
                response_status="success",
                message="",
                data=serializer.data,
                meta={},
            )
        return cached_response(
            request=request,
            status=status.HTTP_400_BAD_REQUEST,
            response_status="failed",
            message="",
            data=serializer.errors,
            meta={},
        )
