from datetime import datetime
import logging


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('RequestLoggingMiddleware')
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log IP address
        ip_address = request.META.get('REMOTE_ADDR')
        
        # Log request body payload
        payload = request.body
        
        # Log cookies
        cookies = request.COOKIES
        
        logger.warn(f'{now} - {ip_address} - {request.method} - {request.path} - Cookies: {cookies} - Payload: {payload.decode()}')
        response = self.get_response(request)
        return response
