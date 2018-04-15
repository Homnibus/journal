from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from ..models import Projet
from .error import Http_status

def recuperer_codex(slug,user,http_status=Http_status()):
    """Récupération du codex en cours et gestion des droits"""
    try:
        #Récupération du codex
        codex = Projet.objects.get(slug=slug)
        #Verification que le codex existe et que le user a le droits de voir le codex
        if codex.createur != user:
            raise PermissionDenied
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
    except Exception as ex:
        raise
        
class Page_Journal():
    def __init__(self, date):
        self.journal_form = None
        self.liste_todo = []
        self.date = date
        self.task_list = []
        self.journal_entry = None
        self.new_task = None
