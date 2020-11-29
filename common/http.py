from django.http import JsonResponse, HttpRequest
from common.forms import JsonModelForm


class ResponseManager:
    def __init__(self, request: HttpRequest = None, messages: list = None,
                 append_user_data: bool = False, **additional_response_data):
        if append_user_data and request is None:
            raise ValueError("make sure you provide `request` or set `append_user_data` to `False`")

        self.append_user_data = append_user_data  # If set True then user data is added, if set `True` additional db query must be made.
        self.messages = messages or {
            "error": [],  # Error message, will be displayed in red.
            "info": [],  # Info message, will be displayed in blue.
            "success": [],  # Success Message, will be displayed in green.
            "warning": []  # Warning Message, will be displayed in yellow.
        }  # list of messages to be send in frontend.
        self.request = request  # For evaluating current user condition.

        if append_user_data:
            # User related info !!
            user_data = {
                "is_logged_in": False,
                "is_superuser": False
            }
        else:
            user_data = {}

        self.response = {
            # message and error handling !!
            "messages": messages,  # For ``non-form field`` related errors.
            "field_errors": {},  # For ``form field`` related errors.
            "has_errors": False,  # For Knowing if the response contains any error.

            # DB/Query/Pagination Related !!
            "pagination": {},
            "has_pagination_data": False,
            **user_data,
            **additional_response_data,
        }

    # For handling db query related !!
    def add_list_view_data(self, response_field_name: str, objects: list, fields: dict):
        """Loops through all the objects and grabs data from fields and appends to list, then add data as provided response_field_name.

        @param response_field_name: adds data as this field in response data.
        @param objects: list of objects.
        @param fields: fields or callable, will be passed to serializer.
        @return: None
        """
        self.response[response_field_name] = [obj.serialize(fields=fields) for obj in objects]  # NOQA

    def add_db_data(self, response_field_name: str, object_, fields: dict):
        """Adds object serialized data to ``response_field_name``

        :param response_field_name: this will be the name of the field in response data.
        :param object_: model object through which the query is made.
        :param fields: fields to be included in the response data
        :return: None
        """
        self.response[response_field_name] = object_.serialize(fields=fields)

    def add_paginator_data(self, paginator=None, page=None):
        """Provides support for paginator, auto adds data  !!

        @param page: assigned page object of django paginator
        @param paginator: django paginator object
        @return: None
        """
        if paginator:
            self.response["pagination"]["total_results"] = paginator.count

        if page:
            if page.has_next():
                self.response["pagination"]["has_next_page"] = True  # NOQA
                self.response["pagination"]["next_page_number"] = page.next_page_number()
            else:
                self.response["pagination"]["has_next_page"] = False  # NOQA

            if page.has_previous():
                self.response["pagination"]["has_previous_page"] = True  # NOQA
                self.response["pagination"]["previous_page_number"] = page.previous_page_number()
            else:
                self.response["pagination"]["has_previous_page"] = False  # NOQA

        self.response["has_pagination_data"] = True

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
    def __add_user_data(self):
        if self.append_user_data:
            # for user related jobs !!
            is_logged_in = self.request.user.is_authenticated
            self.response["is_logged_in"] = is_logged_in

            if is_logged_in:
                self.response["is_superuser"] = self.request.user.is_superuser

    def compile(self, raw, *args, **kwargs):
        """
        Returns dict of response value or JsonResponse object.

        :param raw: if set true raw `dict` will be returned, else JsonResponse will be returned
        :param args: positional arguments accepted by JsonResponse
        :param kwargs: keyword arguments accepted by JsonResponse
        :return: `dict` of response data or JsonResponse object
        """
        self.__add_user_data()
        self.response["has_errors"] = self.has_errors()
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
