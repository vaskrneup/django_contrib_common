from django.http import JsonResponse

from functools import wraps

from common.http import ResponseManager


# User related !!
def user_passes_test(test, failed_return_value: dict):
    """Check if the user passes the test or not, if not then return `JsonResponse` with `failed_return_value` else return `decorated function` !!

    :param test: Accepts function or any data type that can compare to boolean.
    :param failed_return_value: Data to JsonResponse if user doesn't pass the test.
    :return: Decorator or JsonResponse
    """

    def decorator_function(function):
        def __wrapper(request, *args, **kwargs):
            if callable(test):
                test_passed = test(request.user)
            else:
                test_passed = test

            if test_passed:
                return function(request, *args, **kwargs)
            else:
                return JsonResponse(failed_return_value)

        return __wrapper

    return decorator_function


# TODO: "Change hardcoded message."
def login_required(message=None):
    """Check if the user is logged in or not, if not then return `JsonResponse` with `message` else return `decorated function`.

    :param message: Message to be sent if user is not logged in, if not provided then default message(LOGIN_REQUIRED_MESSAGE) will be used.
    :return: Decorator or JsonResponse
    """

    def decorator_function(function):
        @wraps(function)
        def __wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return function(request, *args, **kwargs)
            else:
                res = ResponseManager()
                res.add_warning_message(title="Not Logged In", message="Please Make sure you are logged in.")
                return res()

        return __wrapper

    return decorator_function


def logout_required(message=None):
    """Check if the user is logged in or not, if not then return `JsonResponse` with `message` else return `decorated function`.

    :param message: Message to be sent if user is not logged in, if not provided then default message(LOGOUT_REQUIRED_MESSAGE) will be used.
    :return: Decorator or JsonResponse
    """

    def decorator_function(function):
        @wraps(function)
        def __wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                res = ResponseManager()
                res.add_warning_message(title="Already Logged In", message="Please logout before accessing this page.")
                return res()
            else:
                return function(request, *args, **kwargs)

        return __wrapper

    return decorator_function


# Request related !!
def allow_ajax_only(message=None):
    """Check if the request is ajax or not, if not then return `JsonResponse` with `message` else return `decorated function`.

    @param message: Message to be sent if request is not ajax, if not provided then default message(ALLOW_AJAX_ONLY_MESSAGE) will be used.
    @return: Decorator or JsonResponse
    """

    def decorator(function):
        @wraps(function)
        def __wrapper(request, *args, **kwargs):
            if not request.is_ajax():
                res = ResponseManager()
                res.add_warning_message(
                    title="Not Allowed",
                    message="Request to this page is forbidden, please make sure you use authentic app."
                )
                return res()

            return function(request, *args, **kwargs)

        return __wrapper

    return decorator


def allowed_methods(methods=None, message=None):
    """Check if the request is ajax or not, if not then return `JsonResponse` with `message` else return `decorated function`.

    @param methods: List of allowed methods, if not provided default(["GET", "POST"]) will be used.
    @param message: Message to be sent if request is not in provided methods, if not provided then default message(ALLOWED_METHOD_MESSAGE) will be used.
    @return: Decorator or JsonResponse
    """
    methods = methods or ["GET", "POST"]

    def decorator_function(function):
        @wraps(function)
        def __wrapper(request, *args, **kwargs):
            if request.method in methods:
                return function(request, *args, **kwargs)
            else:
                res = ResponseManager()
                res.add_warning_message(
                    title="Method Not Allowed",
                    message=f"""Available Methods are "{', '.join(methods)}" only"""
                )
                return res()

        return __wrapper

    return decorator_function
