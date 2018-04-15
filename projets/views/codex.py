import json
import logging
from datetime import date,datetime,time

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from ..models import Projet, Journal_Entree, TODO_Entree, get_current_timestamp
from ..forms import Journal_EntreeForm, TODO_EntreeForm
from ..commun.error import Http_status, afficher_erreur, raise_SuspiciousOperation
from ..commun.codex import recuperer_codex, Page_Journal


def get_today_page(codex, aujourdhui):
    """Ajout de la page de journal du jour"""
    #Initialisation de la page du jours et ajout de la date
    page_du_jour = Page_Journal(date=aujourdhui);
    #Récupération l'entre de journal du jour(on genere une entre vide si elle n'existe pas)
    entre_du_jour = Journal_Entree.objects.filter(
        projet=codex,
        date_creation__range=[
            datetime.combine(aujourdhui, time.min),
            datetime.combine(aujourdhui, time.max)
        ]
    ).first()                    
    if entre_du_jour is None:
        entre_du_jour = Journal_Entree(projet=codex)
    #Ajout de l'entre de journal du jour sous la forme de formulaire
    page_du_jour.journal_entry = Journal_EntreeForm(instance=entre_du_jour)
    #Ajout de la tache vide pour création
    page_du_jour.new_task = TODO_EntreeForm();
    #Récupération des taches du jour
    taches_du_jour = list(TODO_Entree.objects.filter(
        projet=codex,
        date_creation__range=[
            datetime.combine(aujourdhui, time.min),
            datetime.combine(aujourdhui, time.max)
        ]
    ).order_by('date_creation'))
    #Ajout des taches à la page courante sous la forme de formulaire
    for tache in taches_du_jour:
        page_du_jour.task_list.append(TODO_EntreeForm(instance=tache))
    #On retourne la page ainsi formé
    return page_du_jour

    
@login_required
def afficher_codex(request,slug):
    """Afficher les entrees d'un codex."""
    http_status = Http_status()
    return_data = {}

    try:
        #Récuperation du codex a affichier
        codex = recuperer_codex(slug,request.user,http_status)
        return_data.update({'codex':codex})

        if request.method == 'GET':
            try:
                #On cherche la date du jour en BDD car les prochaines comparaisons sont faite avec des dates générés par la BDD
                aujourdhui = get_current_timestamp()
                ##Recupération de la page de journal du jour
                page_du_jour = get_today_page(codex, aujourdhui)
                #Ajout de la page de jour au données que l'on retourne
                return_data.update({'today_entry':page_du_jour})            
                ##Ajout des anciennes pages de journal                
                #Initialsiation de la liste des pages
                liste_page_journal = []
                #Récupération des entrees                
                dernieres_journal_entree = list(Journal_Entree.objects.filter(
                    projet=codex,
                    date_creation__lt=datetime.combine(aujourdhui, time.min)
                ).order_by('date_creation'))
                journal_conteur = 0
                #Récupération des taches
                dernieres_todo_entree = TODO_Entree.objects.filter(
                    projet=codex,
                    date_creation__lt=datetime.combine(aujourdhui, time.min)
                ).order_by('date_creation')
                todo_conteur = 0                
                #Generation de la liste des "pages" du journal
                while todo_conteur < len(dernieres_todo_entree) or journal_conteur < len(dernieres_journal_entree):
                    #Calcul de la date  min entre journal et tache
                    if todo_conteur >= len(dernieres_todo_entree):
                        current_date = dernieres_journal_entree[journal_conteur].date_creation.date()
                    elif journal_conteur >= len(dernieres_journal_entree):
                        current_date = dernieres_todo_entree[todo_conteur].date_creation.date()
                    else:
                        current_date = min(
                            dernieres_journal_entree[journal_conteur].date_creation,
                            dernieres_todo_entree[todo_conteur].date_creation
                        ).date()                        
                    #Initialisation de la page courante avec la date calculé
                    current_page_journal = Page_Journal(date=current_date)
                    journal_est_seul = True                    
                    #Ajout de l'entree de journal à la page courante
                    while journal_conteur < len(dernieres_journal_entree) and dernieres_journal_entree[journal_conteur].date_creation.date() == current_date:
                        #TODO :Ajouter la gestion des erreurs lorsque l'on a deux entree de journal pour une même date
                        if journal_est_seul == False:
                            print("ERREUR")
                        current_page_journal.journal_entry = Journal_EntreeForm(instance=dernieres_journal_entree[journal_conteur])
                        journal_conteur += 1
                        journal_est_seul = False                     
                    #Ajout des taches  à la page courante    
                    while todo_conteur < len(dernieres_todo_entree) and dernieres_todo_entree[todo_conteur].date_creation.date() == current_date:
                        current_page_journal.task_list.append(TODO_EntreeForm(instance=dernieres_todo_entree[todo_conteur]))
                        todo_conteur += 1                                    
                    #Ajout de la page à la liste de page final
                    liste_page_journal.append(current_page_journal)
                #Ajout au données qui sont retourné
                return_data.update({'older_entry':liste_page_journal})
                
                ##Envoie de la réponse http
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


@login_required
def maj_todo(request,slug):
    """Met à jour les todo d'un codex."""
    http_status = Http_status()
    return_data = {}

    try:
        #Récuperation du codex a affichier
        codex = recuperer_codex(slug,request.user,http_status)
        if request.method == 'POST' and request.is_ajax():
            try:
                #Boolean qui défini si on est sur une nouvelle tache
                nouvelle_tache = False
                #Récupération du formulaire
                form = TODO_EntreeForm(request.POST)

                if form.is_valid():
                    #Récupération de l'id
                    form_todo_entree = form.save(commit=False)
                    id = form_todo_entree.id
                    #Si nous n'avons pas d'id, c'est que c'est une nouvelle entree à creer
                    if id is None or id == '':
                        nouvelle_tache = True

                    #Récupération de la tache de base
                    if nouvelle_tache:
                        todo_entree = TODO_Entree(projet=codex)
                    else:
                        todo_entree =TODO_Entree.objects.get(id=id)
                    #Maj de la tache
                    todo_entree.texte = form_todo_entree.texte
                    todo_entree.realisee = form_todo_entree.realisee
                    todo_entree.save()

                    #Récupération du html d'un nouveau formulaire avec les données mises à jours pour affichage
                    # et ajout aux données à retourner
                    if nouvelle_tache:
                        out_form = '<table>' + str(TODO_EntreeForm(instance=todo_entree)) + '</table>'                       
                        return_data['out_form'] = out_form

                    #Preparation des données à retourner
                    return_data.update({'success': True, 'id':todo_entree.id, 'nouvelle_tache':nouvelle_tache})
                        
                #Si le formulaire n'est pas valide, on retourne une erreur
                else:
                    form_errors = str(form.non_field_errors) + str(form.texte.errors)
                    return_data.update({
                        'success': False,
                        'form_id': request.POST.get('form_id'),
                        'id': todo_entree.id,
                        'nouvelle_tache':nouvelle_tache,
                        'form_errors':form_errors
                    })
                return JsonResponse(return_data)
            except ObjectDoesNotExist:
                http_status.status = 404
                http_status.message = "La tache n'existe pas."
                http_status.explanation = "La tache que vous voulez accéder n'existe pas."
                raise
            except Exception as ex:
                raise    
        else:
            raise_SuspiciousOperation(http_status)
    except Exception as ex:
        #Retourne l'erreur sous la forme d'une page ou d'un dico json
        return afficher_erreur(request,ex,http_status)
    return HttpResponseForbidden()
