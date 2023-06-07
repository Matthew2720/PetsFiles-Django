from .views import check_notifications


class CheckNotificationsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        check_notifications(request)
        response = self.get_response(request)
        return response
