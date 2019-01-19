import logging
from django.http import JsonResponse
from django.shortcuts import render

from projets.commun.error import HttpError


class PutAndDeleteParsingMiddleware:
    """
    Allow to parse PUT and DELETE request without having to use a REST framework
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if request.method == "PUT":
            if hasattr(request, "_post"):
                del request._post
                del request._files
            try:
                request.method = "POST"
                request._load_post_and_files()
                request.method = "PUT"
            except AttributeError as e:
                request.META["REQUEST_METHOD"] = "POST"
                request._load_post_and_files()
                request.META["REQUEST_METHOD"] = "PUT"

            request.PUT = request.POST
        elif request.method == "DELETE":
            if hasattr(request, "_post"):
                del request._post
                del request._files
            try:
                request.method = "POST"
                request._load_post_and_files()
                request.method = "DELETE"
            except AttributeError as e:
                request.META["REQUEST_METHOD"] = "POST"
                request._load_post_and_files()
                request.META["REQUEST_METHOD"] = "DELETE"

            request.DELETE = request.POST

        return self.get_response(request)


class RequestExceptionHandler:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    @staticmethod
    def process_exception(request, exception):

        logger = logging.getLogger(__name__)

        # Prepare the output data
        output_data = {}
        status_code = 500
        if isinstance(exception, HttpError):
            status_code = exception.status_code
            output_data.update(vars(exception))
            del output_data["status_code"]
            logger.error("Error - " + str(status_code) + " : " + str(exception.message))
            logger.error("Explanation - " + str(exception.explanation))
            logger.exception("Traceback :")
        else:
            output_data.update({"message": "Unexpected error"})
            output_data.update({"explanation": "Unexpected server error"})
            logger.error("Error - 500 : Unexpected Error.")
            logger.exception("Traceback :")

        if request.is_ajax():
            return JsonResponse(output_data, status=status_code)
        else:
            return render(request, "projets/400.html", output_data, status=status_code)
