from django import forms

from common.models import TestModel


class JsonModelForm(forms.ModelForm):
    """Form for managing Json requests"""

    def __init__(self, *args, request=None, **kwargs):
        self._request = request
        self.pre_init()
        super().__init__(*args, **kwargs)
        self.post_init()

    def get_request(self):
        """Gets the request object. If not set ValueError will be raised."""
        if self._request is None:
            raise ValueError(
                "either pass `request` as keyword argument "
                "when initializing the form or use `set_request` to set request"
            )

        return self._request

    def set_request(self, request):
        """Sets the request object."""
        self._request = request

    def pre_init(self):
        """override this for doing something before init !!"""

    def post_init(self):
        """override this for doing something after init !!"""

    def get_errors_format_json(self) -> dict:
        return self.errors.as_json()

    def get_errors(self, format_="json"):
        """
        Returns Error data in JSON format !!
        :param format_: which format to use when returning data !!
        """
        return getattr(self, f"get_errors_format_{format_}")()

    def set_field_attr(self, fields: list, attr: str, value=None):
        """sets value for `fields => field.attr = value` by excluding fields in exclude

        :param fields: fields to set attribute of data
        :param attr: attributes to set
        :param value: value to set in that attribute
        :return: None
        """
        for field in fields:
            setattr(self.fields[field], attr, value)

    def make_fields_required(self, fields):
        """Makes `fields` required."""
        self.set_field_attr(fields, "required", True)


class TestForm(JsonModelForm):
    class Meta:
        model = TestModel
        fields = "__all__"
