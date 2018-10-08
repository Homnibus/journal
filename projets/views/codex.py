import json
import logging
from datetime import date,datetime,time

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache

from ..models import Projet, Journal_Entree, TODO_Entree, get_current_timestamp
from ..forms import Journal_EntreeForm, TODO_EntreeForm
from ..commun.error import Http_status, afficher_erreur, raise_SuspiciousOperation
from ..commun.codex import recuperer_codex, Page_Journal


def get_today_page(codex, aujourdhui):
    """Retourne la Page d'aujourd'hui"""
    #Initialisation de la Page et ajout de la date
    page_du_jour = Page_Journal(date=aujourdhui);
    
    #Récupération de la Note du jour (on genere une entre vide si elle n'existe pas)
    note_du_jour = Journal_Entree.objects.filter(
        projet=codex,
        date_creation__range=[
            datetime.combine(aujourdhui, time.min),
            datetime.combine(aujourdhui, time.max)
        ]
    ).first()                    
    if note_du_jour is None:
        note_du_jour = Journal_Entree(projet=codex)
    
    #Ajout de la Note sous la forme de formulaire
    page_du_jour.journal_entry = Journal_EntreeForm(instance=note_du_jour)
    #Ajout de la Tache vide pour la création de nouvelle Taches
    page_du_jour.new_task = TODO_EntreeForm();
    #Récupération des Taches du jour
    liste_taches_du_jour = list(TODO_Entree.objects.filter(
        projet=codex,
        date_creation__range=[
            datetime.combine(aujourdhui, time.min),
            datetime.combine(aujourdhui, time.max)
        ]
    ).order_by('date_creation'))
    #Ajout des Taches à la Page sous la forme de formulaire
    for tache in liste_taches_du_jour:
        page_du_jour.task_list.append(TODO_EntreeForm(instance=tache))
    
    #On retourne la Page ainsi formé
    return page_du_jour

    
def get_pages_before_today(codex,aujourdhui):
    """Extraction des Pages plus veilles qu'aujourd'hui sous forme de liste"""
    #Initialsiation de la liste des Pages
    liste_old_pages = []
    
    #Récupération de toutes les Notes du codex qui datent d'avant aujourd'hui
    liste_old_notes = list(Journal_Entree.objects.filter(
        projet=codex,
        date_creation__lt=datetime.combine(aujourdhui, time.min)
    ).order_by('date_creation'))
    notes_conteur = 0
    
    #Récupération de toutes les Taches du Codex qui datent d'avant aujourd'hui
    liste_old_taches = TODO_Entree.objects.filter(
        projet=codex,
        date_creation__lt=datetime.combine(aujourdhui, time.min)
    ).order_by('date_creation')
    taches_conteur = 0
    
    #Appareillage des Notes et des Taches en fonction de leur date de création
    while taches_conteur < len(liste_old_taches) or notes_conteur < len(liste_old_notes):
    
        #Calcul de la date min entre Note et Tache
        if taches_conteur >= len(liste_old_taches):
            current_date = liste_old_notes[notes_conteur].date_creation.date()
        elif notes_conteur >= len(liste_old_notes):
            current_date = liste_old_taches[taches_conteur].date_creation.date()
        else:
            current_date = min(
                liste_old_notes[notes_conteur].date_creation,
                liste_old_taches[taches_conteur].date_creation
            ).date()
        
        #Initialisation d'une Page avec la date calculé
        current_page = Page_Journal(date=current_date)
        page_est_seule = True
        
        #Ajout de la Note à la Page
        while notes_conteur < len(liste_old_notes) and liste_old_notes[notes_conteur].date_creation.date() == current_date:
            #TODO :Ajouter la gestion des erreurs lorsque l'on a deux entree de journal pour une même date
            if page_est_seule == False:
                print("ERREUR")
            current_page.journal_entry = Journal_EntreeForm(instance=liste_old_notes[notes_conteur])
            notes_conteur += 1
            page_est_seule = False                     
        
        #Ajout des Taches à la Page
        while taches_conteur < len(liste_old_taches) and liste_old_taches[taches_conteur].date_creation.date() == current_date:
            current_page.task_list.append(TODO_EntreeForm(instance=liste_old_taches[taches_conteur]))
            taches_conteur += 1                                    
        
        #Ajout de la page à la liste de page final
        liste_old_pages.append(current_page)
    
    #On retourne la liste de Pages ainsi formé
    return liste_old_pages

    
@login_required
@never_cache
def afficher_codex(request,slug):
    """Affiche les Pages d'un Codex."""
    http_status = Http_status()
    return_data = {}

    try:
        #Récuperation des infos de base du Codex a affichier
        codex = recuperer_codex(slug,request.user,http_status)
        return_data.update({'codex':codex})

        if request.method == 'GET':
            try:
                #On cherche la date du jour en BDD car les prochaines comparaisons sont faite avec des dates générés par la BDD
                aujourdhui = get_current_timestamp()
                
                #Recupération de la Page d'aujourd'hui
                page_du_jour = get_today_page(codex, aujourdhui)
                #Ajout de la Page du jour aux données que l'on retourne
                return_data.update({'today_entry':page_du_jour})            
                
                #Ajout des anciennes Pages
                liste_old_pages = get_pages_before_today(codex,aujourdhui)
                #Ajout au données qui sont retourné
                return_data.update({'older_entry':liste_old_pages})
                
                #Envoie de la réponse http
                return render(
                    request,
                    'projets/codex.html',
                    return_data
                )
            except Exception as ex:
                raise
        else:
            raise_SuspiciousOperation(http_status)
    except Exception as ex:
        #Retourne l'erreur sous la forme d'une page ou d'un dico json
        return afficher_erreur(request,ex,http_status)
    return HttpResponseForbidden()


@login_required
def maj_journal(request,slug):
    """Met à jour les entrees d'un codex."""
    http_status = Http_status()
    return_data = {}

    try:
        #Récuperation du codex a affichier
        codex = recuperer_codex(slug,request.user,http_status)

        if request.method == 'POST' and request.is_ajax():
            try:
                #Récupération du formulaire
                form = Journal_EntreeForm(request.POST)
                #Récupération de l'id
                id = request.POST.get('id')
                #Boolean qui défini si on est sur une nouvelle tache
                nouveau_journal = False
                
                if form.is_valid():
                    texte = form.save(commit=False).texte
                    #Si nous n'avons pas d'id, c'est que c'est une nouvelle entree à creer
                    if id is None or id == '':
                        #Verification qu'une entree pour la date du jour n'existe pas
                        aujourdhui = get_current_timestamp()
                        journal_entree = Journal_Entree.objects.filter(
                            projet=codex,
                            date_creation__year=aujourdhui.year,
                            date_creation__month=aujourdhui.month,
                            date_creation__day=aujourdhui.day
                        ).first()
                        #Si l'entree n'existe pas on la cree, sinon on l'utilise
                        if journal_entree is None:
                            journal_entree = Journal_Entree(projet=codex)
                            nouveau_journal = True
                    #Sinon c'est une entree deja existante
                    else:
                        journal_entree = Journal_Entree.objects.get(id=id)
                    #Une fois qu'on a la bonne entree, on met a jours le texte et on sauvegarde
                    journal_entree.texte = texte
                    journal_entree.save()
                    
                    #Preparation des données à retourner
                    return_data.update({
                        'success': True,
                        'nouveau_journal': nouveau_journal,
                        'id': journal_entree.id
                    })
                #Si le formulaire n'est pas valide, on retourne une erreur    
                else:
                    form_errors = str(form.non_field_errors) + str(form.texte.errors)
                    return_data.update({
                        'success': False,
                        'id': journal_entree.id,
                        'form_errors':form_errors
                    })
                return JsonResponse(return_data)
            except ObjectDoesNotExist:
                http_status.status = 404
                http_status.message = "L'entree de journal n'existe pas."
                http_status.explanation = "L'entree de journal que vous voulez accéder n'existe pas."
                raise
            except Exception as ex:
                raise
        else:
            raise_SuspiciousOperation(http_status)
    except Exception as ex:
        #Retourne l'erreur sous la forme d'une page ou d'un dico json
        return afficher_erreur(request,ex,http_status)
    return HttpResponseForbidden()

    
def post_tache(codex,form,http_status=Http_status()):
    """Crée une tache d'un codex."""
    return_data = {}

    try:
        if form.is_valid():
        
            form_todo_entree = form.save(commit=False)
            #Si la tache est vide, on ne la crée pas
            if(form_todo_entree.texte and not form_todo_entree.texte.isspace()):
                #Création de la tache
                todo_entree = TODO_Entree(projet=codex,texte=form_todo_entree.texte,realisee=form_todo_entree.realisee)
                todo_entree.save()

                #Récupération du html d'un nouveau formulaire avec les données mises à jours pour affichage
                # et ajout aux données à retourner
                out_form = '<table>' + str(TODO_EntreeForm(instance=todo_entree)) + '</table>'                       

                #Preparation des données à retourner
                return_data.update({'success': True,'out_form': out_form,'id':todo_entree.id})
            else:
                return_data.update({
                    'success': False,
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
    
def put_tache(codex,form,http_status=Http_status()):
    """Met à jour une tache d'un codex."""
    return_data = {}

    try:
        if form.is_valid():
            #Récupération des infos du formulaire
            form_todo_entree = form.save(commit=False)
            #Récupération de la tache (si elle n'existe pas ça léve une erreur qui est géré)
            todo_entree = TODO_Entree.objects.get(id=form_todo_entree.id)
            #Maj de la tache
            todo_entree.texte = form_todo_entree.texte
            todo_entree.realisee = form_todo_entree.realisee
            todo_entree.save()
 
            #Preparation des données à retourner
            return_data.update({'success': True, 'id':todo_entree.id})
                        
        #Si le formulaire n'est pas valide, on retourne une erreur
        else:
            form_errors = str(form.non_field_errors) + str(form.texte.errors)
            return_data.update({
                'success': False,
                'form_id': request.POST.get('form_id'),
                'id': todo_entree.id,
                'form_errors':form_errors
            })
    except ObjectDoesNotExist:
        http_status.status = 404
        http_status.message = "La tache n'existe pas."
        http_status.explanation = "La tache que vous voulez mettre à jour n'existe pas."
        raise
    except Exception as ex:
        raise
    return return_data
    
def delete_tache(codex,form,http_status=Http_status()):
    """Supprime une tache d'un codex."""
    return_data = {}

    try:
        if form.is_valid():
            #Récupération de l'id
            form_todo_entree = form.save(commit=False)
            id = form_todo_entree.id
            TODO_Entree.objects.filter(id=id).delete()

            #Preparation des données à retourner
            return_data.update({'success': True, 'id':id})
                
        #Si le formulaire n'est pas valide, on retourne une erreur
        else:
            form_errors = str(form.non_field_errors) + str(form.texte.errors)
            return_data.update({
                'success': False,
                'form_id': request.POST.get('form_id'),
                'id': todo_entree.id,
                'form_errors':form_errors
            })
    except ObjectDoesNotExist:
        http_status.status = 404
        http_status.message = "La tache n'existe pas."
        http_status.explanation = "La tache que vous voulez accéder n'existe pas."
        raise
    except Exception as ex:
        raise    
    return return_data

def java_string_hashcode(s):
    h = 0
    for c in s:
        h = (31 * h + ord(c)) & 0xFFFFFFFF
    return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000    
    
@login_required
def rest_tache(request,slug):
    """Actions REST sur les taches d'un codex."""
    http_status = Http_status()
    return_data = {}
    
    try:
        #Récuperation du codex a affichier
        codex = recuperer_codex(slug,request.user,http_status)
        if request.method == 'POST' and request.is_ajax():
            #Récupération du formulaire
            form = TODO_EntreeForm(request.POST)
            return_data = post_tache(codex,form,http_status)
        elif request.method == 'PUT' and request.is_ajax():
            #Récupération du formulaire
            request.method = "POST"
            request._load_post_and_files()
            request.method = "PUT"
            form = TODO_EntreeForm(request.POST)
            print(request.POST["hash"])
            print(request.POST["todo_id"])
            print(TODO_Entree.objects.get(id=request.POST["todo_id"]).texte)
            print(java_string_hashcode(TODO_Entree.objects.get(id=request.POST["todo_id"]).texte))
            return_data = put_tache(codex,form,http_status)
        elif request.method == 'DELETE' and request.is_ajax():
            #Récupération du formulaire
            request.method = "POST"
            request._load_post_and_files()
            request.method = "DELETE"
            form = TODO_EntreeForm(request.POST)
            return_data = delete_tache(codex,form,http_status)
        else:
            raise_SuspiciousOperation(http_status)
        #On renvoi la réponse
        return JsonResponse(return_data)
    except Exception as ex:
        #Retourne l'erreur sous la forme d'une page ou d'un dico json
        return afficher_erreur(request,ex,http_status)
    return HttpResponseForbidden()
        
    