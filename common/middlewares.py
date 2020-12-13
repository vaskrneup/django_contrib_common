import json


class JsonToPOSTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.data = None
        _body = request.body

        if request.method == "POST" and not request.FILES:
            try:
                request.data = json.loads(_body)
                if csrf_token := request.data.get("csrfmiddlewaretoken"):
                    request.POST = request.POST.copy()
                    request.POST["csrfmiddlewaretoken"] = csrf_token
            except (AttributeError, json.decoder.JSONDecodeError):
                pass

        res = self.get_response(request)
        return res
