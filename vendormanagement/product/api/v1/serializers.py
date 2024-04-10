from rest_framework import serializers
from django.contrib.auth import get_user_model

from django.core.exceptions import ObjectDoesNotExist


User = get_user_model()

from vendormanagement.product.models import Outlet, Product


class ProductSerializer(serializers.ModelSerializer):
    outlet = serializers.UUIDField(allow_null=True, required=True)

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get("request")
        outlet_uuid = validated_data.pop("outlet", None)
        try:
            outlet = Outlet.objects.get(uuid=outlet_uuid)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Outlet not found")

        validated_data["outlet"] = outlet
        if request and hasattr(request, "user"):
            validated_data["created_by"] = request.user
            validated_data["vendor"] = request.user.vendor
        return super().create(validated_data)

    def get_vendor(self, obj):
        return obj.vendor.uuid

    def get_created_by(self, obj):
        return obj.created_by.uuid


class OutletSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    vendor = serializers.SerializerMethodField()

    class Meta:
        model = Outlet
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["created_by"] = request.user
            validated_data["vendor"] = request.user.vendor
        return super().create(validated_data)

    def get_vendor(self, obj):
        return obj.vendor.uuid

    def get_created_by(self, obj):
        return obj.created_by.uuid


class ProductUnitUpdateSerializer(serializers.Serializer):
    unit = serializers.IntegerField()
    product = serializers.UUIDField(allow_null=True, required=True)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        product_uuid = validated_data.pop("product", None)
        try:
            product = Product.objects.get(uuid=product_uuid)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found")

        if request and hasattr(request, "user"):
            validated_data["modified_by"] = request.user

        product.productSoldUnit = validated_data["unit"]
        product.save()

        return instance
