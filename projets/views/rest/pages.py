from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from ...models import Journal_Entree, get_current_timestamp
from ...forms import Journal_EntreeForm

from ...commun.error import Http_status, afficher_erreur, raise_SuspiciousOperation
from ...commun.codex import recuperer_codex
from ...commun.utils import java_string_hashcode


def post_page(request,codex,http_status):
    """Crée une page d'un codex."""
    return_data = {}
    try:
        #Récupération du formulaire
        form = Journal_EntreeForm(request.POST)
        
        if form.is_valid():
        
            #Verification si une page pour la date du jour existe
            aujourdhui = get_current_timestamp()
            journal_entree = Journal_Entree.objects.filter(
                projet=codex,
                date_creation__year=aujourdhui.year,
                date_creation__month=aujourdhui.month,
                date_creation__day=aujourdhui.day
            ).first()
            
            #Si la page existe déjà, on leve une erreur
            if journal_entree is not None:
                http_status.status = 404
                http_status.message = "La page du jours existe déjà."
                http_status.explanation = "La page que vous voulez créer existe déjà."
                return return_data

            #Creation de la page
            texte = form.save(commit=False).texte
            journal_entree = Journal_Entree(projet=codex,texte=texte)
            journal_entree.save()
            
            #Preparation des données à retourner
            return_data.update({
                'success': True,
                'nouveau_journal': True,
                'id': journal_entree.id
            })
            
        #Si le formulaire n'est pas valide, on retourne une erreur    
        else:
            form_errors = str(form.non_field_errors) + str(form.texte.errors)
            return_data.update({
                'success': False,
                'form_errors':form_errors
            })
            return return_data
    except Exception as ex:
        raise
    return return_data
    
def put_page(request,codex,http_status):
    """Met à jour la page d'un codex."""
    return_data = {}

    try:
        #Récupération du formulaire
        form = Journal_EntreeForm(request.PUT)

        #Récupération de l'id de la page
        id = request.PUT.get('id')
        
        #Récupération du hash de la page
        request_hash = request.PUT.get('hash')
        
        #Si le formulaire n'est pas valide, on retourne une erreur            
        if not form.is_valid():
            form_errors = str(form.non_field_errors) + str(form.texte.errors)
            return_data.update({
                'success': False,
                'id': id,
                'form_errors':form_errors
            })
            return return_data        
            
        #Récupération de la page
        texte = form.save(commit=False).texte
        journal_entree = Journal_Entree.objects.get(id=id)        

        #Si le hash ne correspond pas au texte en base, on retourne une erreur
        #print("request : " + str(request_hash) + " rqst text : |" + texte + "|" + " bdd : " + str(java_string_hashcode(journal_entree.texte)) + "bdd id : " + id +" text : |" + journal_entree.texte + "|")
        if request_hash != str(java_string_hashcode(journal_entree.texte)):
            local_error = "Cette page a été modifié depuis la tentative de mise à jour."
            return_data.update({
                'success': False,
                'id': id,
                'local_error':local_error
            })
            return return_data        
                
        #Une fois qu'on a la bonne page, on met a jours le texte et on sauvegarde
        journal_entree.texte = texte
        journal_entree.save()
        
        #Preparation des données à retourner
        return_data.update({
            'success': True,
            'id': journal_entree.id
        })
            
    except ObjectDoesNotExist:
        http_status.status = 404
        http_status.message = "L'entree de journal n'existe pas."
        http_status.explanation = "L'entree de journal que vous voulez accéder n'existe pas."
        raise
    except Exception as ex:
        raise
    return return_data
    
def delete_page(request,codex,http_status):
    """supprime la page d'un codex."""
    return_data = {}

    try:
        #Récupération de l'id de la page
        id = request.DELETE.get("id")
        
        #Supression de la page
        Journal_Entree.objects.get(id=id).delete()
        
        #Preparation des données à retourner
        return_data.update({
            'success': True,
            'id': id
        })

    except ObjectDoesNotExist:
        http_status.status = 404
        http_status.message = "L'entree de journal n'existe pas."
        http_status.explanation = "L'entree de journal que vous voulez supprimer n'existe pas."
        raise
    except Exception as ex:
        raise
    return return_data
    
@login_required
def rest_page(request,slug):
    """Actions REST sur les pages d'un codex."""
    http_status = Http_status()
    return_data = {}
    
    try:
        #Récuperation du codex lié à la tache
        codex = recuperer_codex(slug,request.user,http_status)

        if request.method == 'POST' and request.is_ajax():
            return_data = post_page(request,codex,http_status)

        elif request.method == 'PUT' and request.is_ajax():
            return_data = put_page(request,codex,http_status)
            
        elif request.method == 'DELETE' and request.is_ajax():
            return_data = delete_page(request,codex,http_status)
            
        else:
            raise_SuspiciousOperation(http_status)
            
        #On renvoi la réponse
        return JsonResponse(return_data)
    except Exception as ex:
        #Retourne l'erreur sous la forme d'une page ou d'un dico json
        return afficher_erreur(request,ex,http_status)
        
    return HttpResponseForbidden()
        
    