import json
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware


class JsonSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        session_key = request.COOKIES.get(
            settings.SESSION_COOKIE_NAME
        ) or request.data.get(
            settings.SESSION_COOKIE_NAME
        )
        request.session = self.SessionStore(session_key)


class JsonToPOSTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.data = {}

        if request.META.get("CONTENT_TYPE") == "application/json":
            try:
                request.data = json.loads(request.body)
                if csrf_token := request.data.get("csrfmiddlewaretoken"):
                    request.POST = request.POST.copy()
                    request.POST["csrfmiddlewaretoken"] = csrf_token
            except (AttributeError, json.decoder.JSONDecodeError):
                pass

        res = self.get_response(request)
        return res
