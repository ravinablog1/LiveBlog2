import logging
import time
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('liveblog')

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
        logger.info(f"Request started: {request.method} {request.path}")

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(f"Request completed: {request.method} {request.path} - {response.status_code} - {duration:.2f}s")
        return response

class ErrorLoggingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        logger.error(f"Exception in {request.method} {request.path}: {str(exception)}", exc_info=True)
        return None