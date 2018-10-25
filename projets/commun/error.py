import logging
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import render
from django.http import JsonResponse


class HttpStatus:
    def __init__(self):
        self.status = 200
        self.message = ""
        self.explanation = ""


def render_error(request, ex, http_status=HttpStatus()):
    logger = logging.getLogger(__name__)
    if http_status.status == 200:
        http_status.status = 500
        http_status.message = "Erreur non prévue."
        http_status.explanation = "Une erreur non prévue c'est produite. Essayez de nouveau et contactez nous si l'erreur persiste."
        logger.error('Erreur ' + str(http_status.status) + ': ' + str(ex))
    else:
        logger.error('Erreur ' + str(http_status.status) + ': ' + str(http_status.explanation))
    if request.is_ajax():
        return JsonResponse(vars(http_status), status=http_status.status)
    else:
        return render(request, 'projets/400.html', vars(http_status), status=http_status.status)


def raise_suspicious_operation(http_status = HttpStatus()):
    http_status.status = 405
    http_status.message = "Méthode de requête non autorisée."
    http_status.explanation = "La méthode de votre requête n'est pas supportée."
    raise SuspiciousOperation
