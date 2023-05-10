from datetime import datetime
import logging


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('RequestLoggingMiddleware')
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        logger.warn(f'{now} {request.method} {request.path}')
        response = self.get_response(request)
        return response
