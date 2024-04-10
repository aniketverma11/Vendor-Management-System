from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model, decorators
from django.utils.translation import gettext_lazy as _

from vendormanagement.users.forms import UserAdminChangeForm, UserAdminCreationForm
from vendormanagement.users.models import Vendor

User = get_user_model()

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://docs.allauth.org/en/latest/common/admin.html#admin
    admin.site.login = decorators.login_required(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": ("name", "first_name", "last_name", "email", "role", "vendor")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = [
        "uuid",
        "username",
        "name",
        "email",
        "get_vendor_name",
        "role",
        "is_superuser",
        "is_active",
        "created",
    ]
    search_fields = ["name", "uuid", "email"]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Check if the 'vendor' field exists in the form
        if "vendor" in form.base_fields:
            form.base_fields["vendor"].required = True
        # Check if the 'role' field exists in the form
        if "role" in form.base_fields:
            form.base_fields["role"].required = True
        return form

    def get_vendor_name(self, obj):
        return obj.vendor.name if obj.vendor else None

    get_vendor_name.short_description = "Vendor Name"


@admin.register(Vendor)
class vendorAdmin(admin.ModelAdmin):
    list_display = ["uuid", "name", "email", "is_active", "created"]
    search_fields = ["name", "uuid", "email"]
