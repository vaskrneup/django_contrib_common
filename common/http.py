from django.http import JsonResponse, HttpRequest
from common.forms import JsonModelForm


class ResponseManager(object):
    def __init__(self, request: HttpRequest = None, messages: list = None, *additional_response_data):
        self.messages = messages or []  # list of messages to be send in frontend.
        self.request = request  # For evaluating current user condition.

        self.response = {
            # message and error handling !!
            "messages": {
                "error": [],  # Error message, will be displayed in red.
                "info": [],  # Info message, will be displayed in blue.
                "success": [],  # Success Message, will be displayed in green.
                "warning": []  # Warning Message, will be displayed in yellow.
            },  # For ``non-form field`` related errors.
            "field_errors": {},  # For ``form field`` related errors.

            # User related info !!
            "is_logged_in": False,
            "is_superuser": False,
            **additional_response_data
        }

    # For handling messages && notification related stuff.
    def __add_message(self, title, message, type_):
        """Internally used for adding message to response data"""
        try:
            self.response["messages"][type_].append({"title": title, "message": message, "type": type_})
        except KeyError:
            raise ValueError(f"support for message type ``{type_}`` not available.")

    def add_error_message(self, title, message):
        """For adding error message to response data."""
        self.__add_message(title, message, "error")

    def add_success_message(self, title, message):
        """For adding success message to response data."""
        self.__add_message(title, message, "success")

    def add_info_message(self, title, message):
        """For adding info message to response data."""
        self.__add_message(title, message, "info")

    def add_warning_message(self, title, message):
        """For adding warning message to response data."""
        self.__add_message(title, message, "warning")

    def add_form_errors(self, form: (JsonModelForm, dict)):
        """Adds field error from ``JsonModelForm`` or provided dict."""
        self.response["field_errors"] = form if type(form) is dict else form.get_errors()
        return self.response["field_errors"]

    def has_errors(self, include_field_errors=False):
        """Checks if there is error in response data."""
        if (include_field_errors and (
                self.response["messages"]["error"] or self.response["field_errors"]
        )) or self.response["messages"]["error"]:
            return True
        else:
            return False

    # For handling final data !!
    def compile(self, raw, *args, **kwargs):
        """
        Returns dict of response value or JsonResponse object.

        :param raw: if set true raw `dict` will be returned, else JsonResponse will be returned
        :param args: positional arguments accepted by JsonResponse
        :param kwargs: keyword arguments accepted by JsonResponse
        :return: `dict` of response data or JsonResponse object
        """
        self.response["has_errors"] = self.has_errors()

        # for user related jobs !!
        is_logged_in = self.request.user.is_authenticated
        self.response["is_logged_in"] = is_logged_in

        if is_logged_in:
            self.response["is_superuser"] = self.request.user.is_superuser

        return self.response if raw else JsonResponse(self.response, *args, **kwargs)

    def __call__(self, raw=False, *args, **kwargs) -> (dict, JsonResponse):
        """

        Returns dict of response value or JsonResponse object, same as calling compile.

        :param raw: if set true raw `dict` will be returned, else JsonResponse will be returned
        :param args: positional arguments accepted by JsonResponse
        :param kwargs: keyword arguments accepted by JsonResponse
        :return: `dict` of response data or JsonResponse object
        """
        return self.compile(raw, *args, **kwargs)

    # For additional Functionality !!
    def __setitem__(self, key, value):
        self.response[key] = value

    def __getitem__(self, item):
        return self.response[item]
