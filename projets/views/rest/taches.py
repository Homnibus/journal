from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from ...models import TODO_Entree
from ...forms import TODO_EntreeForm

from ...commun.error import Http_status, afficher_erreur, raise_SuspiciousOperation
from ...commun.codex import recuperer_codex
from ...commun.utils import java_string_hashcode

def post_tache(request,codex,http_status=Http_status()):
    """Crée une tache d'un codex."""
    return_data = {}
    try:
        #Récupération du formulaire 
        form = TODO_EntreeForm(request.POST)
        
        if form.is_valid():
        
            #Récupération des informations du formulaire
            form_todo_entree = form.save(commit=False)
            
            #Si la tache n'est pas vide on la crée
            if(form_todo_entree.texte and not form_todo_entree.texte.isspace()):
            
                #Création de la tache
                todo_entree = TODO_Entree(
                    projet=codex,
                    texte=form_todo_entree.texte,
                    realisee=form_todo_entree.realisee
                )
                todo_entree.save()

                #Récupération du html d'un nouveau formulaire avec les données mises à jours pour affichage
                # et ajout aux données à retourner
                out_form = '<table>' + str(TODO_EntreeForm(instance=todo_entree)) + '</table>'                       

                #Preparation des données à retourner
                return_data.update({
                    'success': True,
                    'out_form': out_form,
                    'id':todo_entree.id
                })
                
            else:
                local_error = "Impossible de créer une tache vide"
                return_data.update({
                    'success': False,
                    'id': form_todo_entree.id,
                    'local_error':local_error
                })

        #Si le formulaire n'est pas valide, on retourne une erreur
        else:
            form_errors = str(form.non_field_errors) + str(form.texte.errors)
            return_data.update({
                'success': False,
                'form_errors':form_errors
            })

    except Exception as ex:
        raise
    return return_data
    
def put_tache(request,codex,http_status=Http_status()):
    """Met à jour une tache d'un codex."""
    return_data = {}

    try:
        #Récupération du formulaire
        form = TODO_EntreeForm(request.PUT)
        
        #Récupération de l'id de la page
        id = request.PUT.get('id')
        
        #Récuperation du hash de la page
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
        
        #Récupération de la tache (si elle n'existe pas ça léve une erreur qui est géré)
        texte = form.save(commit=False).texte
        realisee = form.save(commit=False).realisee
        todo_entree = TODO_Entree.objects.get(id=id)
        
        #Si le hash ne correspond pas au texte en base, on retourne une erreur
        print("request : " + str(request_hash) + " rqst text : |" + texte + "|" + " bdd : " + str(java_string_hashcode(todo_entree.texte)) + "bdd id : " + id +" text : |" + todo_entree.texte + "|")
        if request_hash != str(java_string_hashcode(todo_entree.texte)):
            local_error = "Cette page a été modifié depuis la tentative de mise à jour."
            return_data.update({
                'success': False,
                'id': id,
                'local_error':local_error
            })
            return return_data        
        
        #Une fois qu'on est sur de ce qu'on va mettre à jour, on le fait et on sauvegarde
        todo_entree.texte = texte
        todo_entree.realisee = realisee
        todo_entree.save()

        #Preparation des données à retourner
        return_data.update({
            'success': True,
            'id':todo_entree.id
        })
                    
        
    except ObjectDoesNotExist:
        http_status.status = 404
        http_status.message = "La tache n'existe pas."
        http_status.explanation = "La tache que vous voulez mettre à jour n'existe pas."
        raise
    except Exception as ex:
        raise
    return return_data
    
def delete_tache(request,codex,http_status=Http_status()):
    """Supprime une tache d'un codex."""
    return_data = {}

    try:
        #Récupération de l'id de la page
        id = request.DELETE.get("id")
            
        #Supression de la tache
        TODO_Entree.objects.filter(id=id).delete()

        #Preparation des données à retourner
        return_data.update({
            'success': True,
            'id':id
        })
                
    except ObjectDoesNotExist:
        http_status.status = 404
        http_status.message = "La tache n'existe pas."
        http_status.explanation = "La tache que vous voulez accéder n'existe pas."
        raise
    except Exception as ex:
        raise    
    return return_data
    
@login_required
def rest_tache(request,slug):
    """Actions REST sur les taches d'un codex."""
    http_status = Http_status()
    return_data = {}
    
    try:
        #Récuperation du codex lié à la tache
        codex = recuperer_codex(slug,request.user,http_status)
        
        if request.method == 'POST' and request.is_ajax():
            return_data = post_tache(request,codex,http_status)
            
        elif request.method == 'PUT' and request.is_ajax():
            return_data = put_tache(request,codex,http_status)
            
        elif request.method == 'DELETE' and request.is_ajax():
            return_data = delete_tache(request,codex,http_status)
            
        else:
            raise_SuspiciousOperation(http_status)
            
        #On renvoi la réponse
        return JsonResponse(return_data)
    except Exception as ex:
        #Retourne l'erreur sous la forme d'une page ou d'un dico json
        return afficher_erreur(request,ex,http_status)
    return HttpResponseForbidden()
        
    