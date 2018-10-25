from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from ..models import Projet
from .error import HttpStatus

def get_codex_from_slug(slug, user, http_status=HttpStatus()):
    """Récupération du codex en cours et gestion des droits"""
    try:
        #Récupération du codex
        codex = Projet.objects.get(slug=slug)
        #Verification que le codex existe et que le user a le droits de voir le codex
        #if codex.createur != user:
        #    raise PermissionDenied
        #Si aucune erreur, on retourne le codex
        return codex
    except ObjectDoesNotExist:
        http_status.status = 404
        http_status.message = "Le codex n'existe pas."
        http_status.explanation = "Le codex que vous voulez accéder n'existe pas."
        raise
    except PermissionDenied:
        http_status.status = 403
        http_status.message = "Permission refusée."
        http_status.explanation = "Vous n'avez pas le droits d'accéder à ce codex."
        raise
    except Exception:
        raise


class Page:
    def __init__(self, date):
        self.date = date
        self.note_form = None
        self.new_task_form = None
        self.tasks_form = []
