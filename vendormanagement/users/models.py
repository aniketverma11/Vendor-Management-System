from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, ForeignKey, CASCADE
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from utils.behaviours import (
    UUIDMixin,
    MobileMixin,
    ImageMixin,
    UserStampedMixin,
    StatusMixin,
    EmailMixin,
)


class Vendor(UUIDMixin, MobileMixin, EmailMixin, StatusMixin):
    name = CharField(_("Name of Vendor"), blank=True, max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"


class User(AbstractUser, UUIDMixin, ImageMixin, MobileMixin):
    """
    Default custom user model for vendorManagement.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    USER_ROLE_CHOICES = (
        ("admin", "admin"),
        ("supervisor", "supervisor"),
        ("salesperson", "salesperson"),
        ("customer", "customer"),
    )

    # First and last name do not cover name patterns around the globe
    vendor = ForeignKey(Vendor, on_delete=CASCADE, blank=True, null=True)
    role = CharField(
        _("User Role"), max_length=100, choices=USER_ROLE_CHOICES, blank=True
    )
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = CharField(_("First Name of User"), blank=True, max_length=255)
    last_name = CharField(_("Last Name of User"), blank=True, max_length=255)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
