import uuid as uuid
from django.db import models

from django.conf import settings
from model_utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


from .managers import StatusMixinManager
from .utils import upload_location, validator_ascii


class StatusMixin(models.Model):
    is_active = models.BooleanField(default=True, blank=False, null=False)
    is_deleted = models.BooleanField(default=False, blank=False, null=False)

    objects = StatusMixinManager()

    def activate(self):
        if not self.is_active:
            self.is_active = True
            self.save()

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.save()

    def remove(self):
        if not self.is_deleted:
            self.is_deleted = True
            self.save()

    def has_changed(self, field):
        model = self.__class__.__name__
        return getattr(self, field) != getattr(
            self, "_" + model + "__original_" + field
        )

    def save(self, *args, **kwargs):
        """
        Makes sure that the ``is_active`` is ``False`` when ``is_deleted`` is ``True``.
        """
        if self.is_deleted:
            self.is_active = False
        super(StatusMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class EmailMixin(models.Model):
    email = models.EmailField(max_length=70, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        abstract = True


class AddressMixin(models.Model):
    address = models.TextField(
        _("Address Line 1"),
        max_length=100,
        blank=True,
        null=True,
        validators=[validator_ascii],
        help_text="The length of this field can't be longer than 100",
    )
    state = models.ForeignKey("core.State", models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey("core.City", models.SET_NULL, blank=True, null=True)
    pin_code = models.ForeignKey("core.PINCode", models.SET_NULL, blank=True, null=True)

    def get_address(self):
        address = ""
        if self.address:
            address += self.address
        if self.city and self.city.name:
            address += ", " + self.city.name
            if self.city.state and self.city.state.name:
                address += ", " + self.city.state.name
                if self.city.state.country and self.city.state.country.name:
                    address += ", " + self.city.state.country.name
        if self.pin_code:
            address += " - " + str(self.pin_code.value)

        if address == "":
            return None
        else:
            return "".join([i if ord(i) < 128 else " " for i in address])

    class Meta:
        abstract = True


class MobileMixin(models.Model):
    mobile = models.CharField(
        blank=True,
        null=True,
        max_length=10,
        help_text="Enter a valid 10 digit mobile number.",
    )
    country_code = models.CharField(
        blank=True,
        null=True,
        max_length=5,
        help_text="Enter a valid country code.",
    )

    class Meta:
        abstract = True


class UUIDMixin(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class ProfileMixin(AddressMixin, MobileMixin, StatusMixin, UUIDMixin):
    date_of_birth = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True


class UserStampedMixin(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="created_%(class)s",
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="updated_%(class)s",
    )

    class Meta:
        abstract = True


class ImageMixin(models.Model):
    image = models.ImageField(
        _("image"), upload_to=upload_location, null=False, blank=False
    )
    image_alt = models.CharField(
        _("image alt"), max_length=100, blank=True, validators=[validator_ascii]
    )

    class Meta:
        abstract = True
