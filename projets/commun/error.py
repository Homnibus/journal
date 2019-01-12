import logging
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.translation import gettext


class HttpStatus:
    def __init__(self):
        self.status = 200
        self.message = ""
        self.explanation = ""


def render_error(request, ex, http_status=HttpStatus()):
    """
    Return an error to the user depending of the http request method
    """
    logger = logging.getLogger(__name__)
    # If the http_status.status is still at 200, it's because it as not been manually updated.
    # As every expected error populate the http_status object, it means that it's a unexpected error.
    if http_status.status == 200:
        http_status.status = 500
        http_status.message = gettext("Unexpected error.")
        http_status.explanation = gettext(
            "An unexpected error append. Try again and if the error persist please "
            "contact us."
        )
        logger.error("Error - " + str(http_status.status) + " : " + str(ex))
    else:
        logger.error(
            "Error - " + str(http_status.status) + " : " + str(http_status.explanation)
        )
    # Return the error depending of the http request method
    if request.is_ajax():
        return JsonResponse(vars(http_status), status=http_status.status)
    else:
        return render(
            request, "projets/400.html", vars(http_status), status=http_status.status
        )


def raise_suspicious_operation(http_status=HttpStatus()):
    """
    Raise a Suspicious Operation error and populate the http_status object.
    """
    http_status.status = 405
    http_status.message = gettext("This HTTP request method is not allowed.")
    http_status.explanation = gettext(
        "The HTTP method of your request is not supported."
    )
    raise SuspiciousOperation
