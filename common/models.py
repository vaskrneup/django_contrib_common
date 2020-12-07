from django.db import models
from django.utils.text import gettext_lazy as __, slugify
from django.contrib.humanize.templatetags import humanize
from django.http.request import HttpRequest
from django.contrib.auth.models import AbstractUser

import uuid
import secrets

from . import utils
from . import validators
from .constants import COUNTRY_CODE


class AbstractBaseModel(models.Model):
    """Abstract Base model to inherit from, it makes sure every model has time stamp."""
    creation_date = models.DateTimeField(
        verbose_name=__("Creation Date"),
        help_text=__("Date of creation of the object."),
        auto_now_add=True,
    )
    update_date = models.DateTimeField(
        verbose_name=__("Last Update Date"),
        help_text=__("Last update date of the object."),
        auto_now=True
    )

    # Meta and initial data.
    class Meta:
        abstract = True

    def __int__(self, *args, **kwargs):
        self._request = None
        super().__init__(*args, **kwargs)

    def set_request(self, request: HttpRequest) -> None:
        """...

        Sets request object.

        :param request: HttpRequest
        :return: None
        """
        self._request = request

    def get_request(self) -> HttpRequest:
        """...

        gets the django HttpRequest object.

        :return: HttpResponse
        """
        assert self._request is not None, "Call ``set_request(request: HttpRequest)`` with django request object to get request."
        return self._request

    # Better Data representation and shortcuts !!
    def humanized_creation_date(self) -> str:
        """Provides human readable creation time"""
        return humanize.naturaltime(self.creation_date)

    def humanized_update_date(self) -> str:
        """Provides human readable update time"""
        return humanize.naturaltime(self.update_date)

    # Functions to override !!
    def get_excluded_fields(self) -> set:
        """
        This will be called internally to get excluded fields,
        the fields returned from it will always be excluded if some data is to be returned.
        """

    # Core functions !!
    def is_new(self):
        """To check if the field is new or not."""
        return self._state.adding

    def get_fields(self, as_list=False, include_parents=True, include_hidden=False) -> (dict, list):
        """
        Return a list of fields associated to the model. By default, include
        forward and reverse fields, fields derived from inheritance, but not
        hidden fields. The returned fields can be changed using the parameters:

        :param as_list: by default data is returned as `dict`, if set `True` `list` is returned
        :param include_parents: include fields derived from inheritance
        :param include_hidden:  include fields that have a related_name that starts with a "+"
        :return: list or dict
        """
        fields = self._meta.get_fields(include_parents, include_hidden)
        return fields if as_list else {key: key for key in fields}

    def serialize_json(self, fields):
        return {
            frontend_field: utils.get_attr(self, fields[frontend_field])
            for frontend_field in fields
        }

    def serialize(self, fields: dict = None, exclude: iter = None, format_: str = "json") -> dict:
        """Provides json data depending on the fields provided.

        ** fields must be of type dict, mapping frontend required fields with backend model callable or property **

        :param fields: `dict of fields` or `callable` to include,
                       where key is frontend field name and value is `model property` or `callable`
        :param exclude: set of fields in model to exclude
        :param format_: format in which the data must be returned
        :return: obj data in json format
        """
        fields = fields if fields is not None else self.get_fields()
        if _exclude := self.get_excluded_fields() is not None:
            exclude = {*_exclude, exclude}
        if exclude:
            for field in exclude:
                try:
                    del fields[field]
                except KeyError:
                    pass

        return getattr(self, f"serialize_{format_}")(fields)


class AbstractBaseUUIDModel(AbstractBaseModel):
    """Model with all functionality and fields from AbstractModel but pk datatype changed to `uuid`."""
    id = models.UUIDField(
        verbose_name=__("Primary Key with unique identifiers."),
        help_text=__(
            "Generates unique identifiers everytime a new object is created."
        ),
        primary_key=True,
        unique=True,
        auto_created=True,
        default=uuid.uuid4,
        editable=False,
        error_messages={
            "invalid": __("Please provide a valid name.")
        }
    )

    class Meta:
        abstract = True


class AbstractBaseSlugModel(AbstractBaseModel):
    """Model with all functionality and fields from AbstractModel with addition of `slug`."""
    SLUG_FROM_FIELD = None

    slug = models.SlugField(
        verbose_name=__("Slug"),
        help_text=__("For Better representation in url"),
        unique=True,
        blank=True
    )

    class Meta:
        abstract = True

    def get_slug_value(self):
        """will be used internally to get slug value, override this to return any slug value you wish."""
        assert self.SLUG_FROM_FIELD is not None, "Either set a constant ``SLUG_FROM_FIELD``, or override ``get_slug_value``, or set value for slug before calling save()"

        return slugify(str(utils.get_attr(self, self.SLUG_FROM_FIELD)) + "-" + secrets.token_hex(7))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug_value()
        super().save(*args, **kwargs)


class AbstractBaseSlugUUIDModel(AbstractBaseSlugModel):
    """Model with all functionality and fields from AbstractModel with addition of `slug` and pk is changed to 'UUID type'."""

    id = models.UUIDField(
        verbose_name=__("Primary Key with unique identifiers."),
        help_text=__(
            "Generates unique identifiers everytime a new object is created."
        ),
        primary_key=True,
        unique=True,
        auto_created=True,
        default=uuid.uuid4,
        editable=False,
        error_messages={
            "invalid": __("Please provide a valid name.")
        }
    )

    class Meta:
        abstract = True


class AbstractCommonUser(AbstractUser):
    DEFAULT_PROFILE_PICTURE_PATH = "common/static/common/default/default.jpg"
    PROFILE_PICTURE_UPLOAD_PATH = "media/profile_picture/"

    username_validator = validators.WordNumberLetterUnderscoreAndDotOnlyValidator()
    phonenumber_validator = validators.InternationalPhoneNumberValidator()

    username = models.CharField(
        verbose_name=__('username'),
        max_length=150,
        unique=True,
        help_text=__(
            'Enter a valid username. This value may contain only letters, '
            'numbers, and (_, .) characters.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': __("A user with that username already exists."),
        },
    )
    phone_number = models.CharField(
        verbose_name=__("Phone Number"),
        max_length=15,
        unique=True,
        help_text=__(
            "Enter a valid number in international or national format."
        ),
        validators=[phonenumber_validator],
        error_messages={
            'unique': __("A user with that phone number already exists."),
        },
    )

    profile_picture = models.ImageField(
        verbose_name=__("Profile Picture"),
        help_text=__(
            "Profile Picture of the user"
        ),
        default=DEFAULT_PROFILE_PICTURE_PATH,
        upload_to=PROFILE_PICTURE_UPLOAD_PATH
    )

    country = models.CharField(
        verbose_name=__("Country"),
        help_text=__("Country of residence."),
        max_length=3,
        blank=True,
        null=True,
        choices=COUNTRY_CODE
    )

    class Meta:
        abstract = True

# class TestModel(AbstractCommonUser):
#     pass
