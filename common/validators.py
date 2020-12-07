from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.text import gettext_lazy as __


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
