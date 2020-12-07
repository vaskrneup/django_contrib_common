from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.text import gettext_lazy as __
from django.core.exceptions import ValidationError

import os


@deconstructible
class WordNumberLetterUnderscoreAndDotOnlyValidator(validators.RegexValidator):
    regex = r'^(?=.{4,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$'
    message = __(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and (_, .) characters.'
    )
    flags = 0


@deconstructible
class InternationalPhoneNumberValidator(validators.RegexValidator):
    regex = r"^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"
    message = __(
        "Enter a valid number in international or national format."
    )
    flags = 0


def validate_file_extension(valid_file_extensions, error_message='Unsupported file extension.'):
    """checks if file extension lies in `valid_file_extensions`."""

    def _validate_file_extension(value):
        try:
            ext = os.path.splitext(value.name)[1]
            if not ext.lower() in valid_file_extensions:
                raise ValidationError(error_message)
        except Exception as _:
            raise ValidationError(error_message)

    return _validate_file_extension
