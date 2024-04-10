# standard import
import logging

from django.core.validators import RegexValidator
from django.utils import timezone
from django.conf import settings
from django.core import signing

# Third-party imports
from random import choice
from string import digits, ascii_lowercase
from rest_framework import status


validator_ascii = RegexValidator(
    regex=r"^[\x00-\x7F]*$", message="Only ASCII characters allowed"
)
validator_pan_no = RegexValidator(
    regex=r"^[A-Z]{5}\d{4}[A-Z]$", message="Please provide a valid pan number"
)

logger = logging.getLogger()


def upload_location(instance, filename):
    ext_set = filename.split(".")
    model = str(instance.__class__.__name__).lower()
    return "%s/%s.%s" % (model, timezone.now(), ext_set[-1])


def generate_random_string(length=5):
    digit_len = length // 2
    alpha_len = length - digit_len
    return "".join(
        [choice(digits) for _ in range(digit_len)]
        + [choice(ascii_lowercase) for _ in range(alpha_len)]
    )


def generate_response_dict(status="error", data={}, meta={}, message="no message"):
    return {"status": status, "message": message, "data": data, "meta": meta}


def string_encrypt(string):
    value = signing.dumps(string)
    return value


def decrypt_string(string):
    value = signing.loads(string)
    return value


def generate_response_dict(status="error", data={}, meta={}, message="no message"):
    return {"status": status, "message": message, "data": data, "meta": meta}


def get_set_password_subject_message(id, frontend_redirect_url):
    subject = "Reset Your Password"
    # Construct the message with a link to set the password
    message = f'<p>Click the link here and set the password<a href="{frontend_redirect_url}{id}"/"">Click Here!</a></p>'
    return {"subject": subject, "message": message}


def get_subscription_request_subject_message(id, frontend_redirect_url):
    subject = "Subscription Request Approval"
    # Construct the message with a link to set the password
    message = f'<p>Thank you for subscribing Click the link here and set the password<a href="{frontend_redirect_url}{id}"/">Click Here!</a></p>'
    return {"subject": subject, "message": message}
