import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings

from ...models import Vendor

User = get_user_model()


class CreateUserProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email").lower()  # Normalize email to lowercase
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        password = data.get("password")

        if User.objects.filter(mobile=data["phone_number"]).exists():
            raise serializers.ValidationError(
                "User with this mobile number  already exists"
            )

        # Email validation
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, email):
            raise serializers.ValidationError("Invalid email format")

        if User.objects.filter(email=data["email"].lower()).exists():
            raise serializers.ValidationError(
                "User with this email {} already exists".format(data["email"])
            )

        # First name validation
        name_regex = r"^[a-zA-Z]+$"
        if not re.match(name_regex, first_name):
            raise serializers.ValidationError("First name can contain only alphabets")

        # Last name validation
        name_regex = r"^[a-zA-Z\'.]+$"
        if not re.match(name_regex, last_name):
            raise serializers.ValidationError(
                "Last name can contain only alphabets, single quote, and dot"
            )

        # Password validation
        password_regex = r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,12}$"
        if not re.match(password_regex, password):
            raise serializers.ValidationError("Invalid password format")

        return data

    def create(self, validated_data):
        user_object = User.objects.create_user(
            username=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            name=validated_data["first_name"] + validated_data["last_name"],
            email=validated_data["email"],
            role="customer",
            mobile=validated_data["phone_number"],
            password=validated_data["password"],
            is_active=True,
        )

        return user_object


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "uuid",
            "email",
            "mobile",
            "first_name",
            "last_name",
            "role",
        ]


class UpdateUserProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    address = serializers.CharField()
    phone_number = serializers.CharField()

    def validate(self, data):
        if User.objects.filter(mobile=data["phone_number"]).exists():
            raise serializers.ValidationError(
                "User with this mobile number  already exists"
            )

        return data


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            # Retrieve the user object based on the provided email
            user = User.objects.get(email=data["email"].lower())
        except:
            raise serializers.ValidationError(
                "User with this email {} not exists".format(data["email"])
            )

        # Check if the provided password matches the user's password
        if user.check_password(data["password"]):
            return data

        else:
            raise serializers.ValidationError("invalid password ")


class LoginResponseSerializer(serializers.Serializer):
    vendor = serializers.SerializerMethodField(read_only=True)
    user_profile = serializers.SerializerMethodField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    access_token = serializers.CharField(read_only=True)

    def get_user_profile(self, profile):
        # Check the user_type field of the user_profile object
        if profile["user_profile"]:
            # If user_type is 10 (organization), serialize using OrganizationProfileSerializer
            return UserProfileSerializer(profile["user_profile"]).data

        else:
            return None

    def get_vendor(self, profile):
        # Check the user_type field of the user_profile object
        if profile["vendor"]:
            # If user_type is 10 (organization), serialize using OrganizationProfileSerializer
            return VendorSerializer(profile["vendor"]).data

        else:
            return None


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims if needed
        # token['claim'] = value

        return token
