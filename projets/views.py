import itertools
import json
import logging
from datetime import date,datetime,time

from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, SuspiciousOperation

from .models import Projet, Main_Courante, Contact_Liste, Journal_Entree, TODO_Entree, get_current_timestamp
from .forms import (ProjetForm, Main_CouranteForm, Contact_ListeForm, Journal_EntreeForm, TODO_EntreeForm)

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Http_status():
    def __init__(self):
        self.status = 200
        self.message = ""
        self.explanation = ""

def afficher_erreur(request,ex,http_status=Http_status()):
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

def raise_SuspiciousOperation(http_status=Http_status()):
    http_status.status = 405
    http_status.message = "Méthode de requête non autorisée."
    http_status.explanation = "La méthode de votre requête n'est pas supportée."
    raise SuspiciousOperation

def recuperer_projet(slug,user,http_status=Http_status()):
    """Récupération du projet en cours et gestion des droits"""
    try:
        #Récupération du projet
        projet = Projet.objects.get(slug=slug)
        #Verification que le projet existe et que le user a le droits de voir le projet
        if projet.createur != user:
            raise PermissionDenied
        #Si aucune erreur, on retourne le projet
        return projet
    except ObjectDoesNotExist:
        http_status.status = 404
        http_status.message = "Le projet n'existe pas."
        http_status.explanation = "Le projet que vous voulez accéder n'existe pas."
        raise
    except PermissionDenied:
        http_status.status = 403
        http_status.message = "Permission refusée."
        http_status.explanation = "Vous n'avez pas le droits d'accéder à ce projet."
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
       
@login_required
def creer_projet(request):
    """Affiche un projet pour creation."""
    http_status = Http_status()
    return_data = {}
    
    try:
        if request.method == 'GET' or request.method == 'POST':
            form = ProjetForm(request.POST or None)
            return_data.update({'form':form})
            if form.is_valid():
                projet = form.save(commit=False)
                projet.createur = request.user
                projet.save()
                return_data.update({'projet':projet})
                return redirect('afficher_projet', slug=projet.slug)
            return render( request, 'projets/nouveau_codex.html', return_data)
        else:
            raise_SuspiciousOperation(http_status)    
    except Exception as ex:
        #Retourne l'erreur sous la forme d'une page ou d'un dico json
        return afficher_erreur(request,ex,http_status)
    return HttpResponseForbidden()
        


@login_required
def afficher_projet(request,slug):
    """Afficher les entrees d'un projet."""
    http_status = Http_status()
    return_data = {}

    try:
        #Récuperation du projet a affichier
        projet = recuperer_projet(slug,request.user,http_status)
        return_data.update({'projet':projet})

        if request.method == 'GET':
            try:                
                ##Ajout de la page de journal du jour
                #On cherche la date en BDD car les prochaines comparaisons sont faite avec des dates générés par la BDD
                aujourdhui = get_current_timestamp()
                #Initialisation de la page du jours et ajout de la date
                page_du_jour = Page_Journal(date=aujourdhui);
                #Récupération de l'entre de journal du jour(on genere une entre vide si elle n'existe pas)
                entre_du_jour = Journal_Entree.objects.filter(
                    projet=projet,
                    date_creation__range=[
                        datetime.combine(aujourdhui, time.min),
                        datetime.combine(aujourdhui, time.max)
                    ]
                ).first()                    
                if entre_du_jour is None:
                    entre_du_jour = Journal_Entree(projet=projet)
                #Ajout de l'entre de journal du jour sous la forme de formulaire
                page_du_jour.journal_entry = Journal_EntreeForm(instance=entre_du_jour)
                #Ajout de la tache vide pour création
                page_du_jour.new_task = TODO_EntreeForm();
                #Récupération des taches du jour
                taches_du_jour = list(TODO_Entree.objects.filter(
                    projet=projet,
                    date_creation__range=[
                        datetime.combine(aujourdhui, time.min),
                        datetime.combine(aujourdhui, time.max)
                    ]
                ).order_by('date_creation'))
                #Ajout des taches à la page courante sous la forme de formulaire
                for tache in taches_du_jour:
                    page_du_jour.task_list.append(TODO_EntreeForm(instance=tache))
                #Ajout de la page de jour au données que l'on retourne
                return_data.update({'today_entry':page_du_jour})
                
                ##Ajout des anciennes pages de journal                
                #Initialsiation de la liste des pages
                liste_page_journal = []
                #Récupération des entrees                
                dernieres_journal_entree = list(Journal_Entree.objects.filter(
                    projet=projet,
                    date_creation__lt=datetime.combine(aujourdhui, time.min)
                ).order_by('date_creation'))
                journal_conteur = 0
                #Récupération des taches
                dernieres_todo_entree = TODO_Entree.objects.filter(
                    projet=projet,
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
    """Met à jour les entrees d'un projet."""
    http_status = Http_status()
    return_data = {}

    try:
        #Récuperation du projet a affichier
        projet = recuperer_projet(slug,request.user,http_status)

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
                            projet=projet,
                            date_creation__year=aujourdhui.year,
                            date_creation__month=aujourdhui.month,
                            date_creation__day=aujourdhui.day
                        ).first()
                        #Si l'entree n'existe pas on la cree, sinon on l'utilise
                        if journal_entree is None:
                            journal_entree = Journal_Entree(projet=projet)
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
    """Met à jour les todo d'un projet."""
    http_status = Http_status()
    return_data = {}

    try:
        #Récuperation du projet a affichier
        projet = recuperer_projet(slug,request.user,http_status)
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
                        todo_entree = TODO_Entree(projet=projet)
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


@login_required
def afficher_main_courante(request,slug):
    """ Afficher la main courante d'un projet."""
    http_status = Http_status()
    return_data = {}

    try:
        #Récuperation du projet a affichier et des droits
        projet = recuperer_projet(slug,request.user,http_status)

        if request.method == 'GET':
            main_courante = Main_Courante.objects.filter(projet=projet).first()
            form = Main_CouranteForm(instance=main_courante)
            return render(request, 'projets/codex_info.html', {'projet':projet,'form':form,'main_courante':main_courante})    
        else:
            raise_SuspiciousOperation(http_status)
    except Exception as ex:
        #Retourne l'erreur sous la forme d'une page ou d'un dico json
        return afficher_erreur(request,ex,http_status)
    return HttpResponseForbidden()

    
@login_required
def maj_main_courante(request,slug):
    """ Modifier la main courante d'un projet."""
    http_status = Http_status()
    return_data = {}
    
    try:
        #Récuperation du projet a affichier et des droits
        projet = recuperer_projet(slug,request.user,http_status)
        
        if request.method == 'POST' and request.is_ajax():
            form = Main_CouranteForm(request.POST)
            if form.is_valid():
                #TODO : Ajouter la gestion d'erreur lors d'un formulaire non
                #       valide (a voir dans quel ca ça arrive)
                main_courante, created = Main_Courante.objects.update_or_create(
                    projet=projet,
                    defaults={'projet':projet,'texte':form.save(commit=False).texte}
                )
                return_data.update({
                    'success': True,
                    'date_update': main_courante.date_update.strftime('%Y-%m-%d %H:%M')
                })
                return JsonResponse(return_data)
        else:
            raise_SuspiciousOperation(http_status)
    except Exception as ex:
        #Retourne l'erreur sous la forme d'une page ou d'un dico json
        return afficher_erreur(request,ex,http_status)
    return HttpResponseForbidden()

    
@login_required
def afficher_contact_liste(request,slug):
    """Affiche la liste de contact d'un projet"""
    http_status = Http_status()
    return_data = {}
    
    try:
        #Récuperation du projet a affichier et des droits
        projet = recuperer_projet(slug,request.user,http_status)

        if request.method == 'GET':
            #TODO : Ajouter la gestion d'erreur lors de plusieurs main courantes
            contact_liste = Contact_Liste.objects.filter(projet=projet).first()
            form = Contact_ListeForm(instance=contact_liste)    
            return render(request, 'projets/codex_contacts.html', {'projet':projet,'form':form,'contact_liste':contact_liste})
        else:
            raise_SuspiciousOperation(http_status)        
    except Exception as ex:
        #Retourne l'erreur sous la forme d'une page ou d'un dico json
        return afficher_erreur(request,ex,http_status)
    return HttpResponseForbidden()

    
@login_required
def maj_contact_liste(request,slug):
    """Affiche la liste de contact d'un projet"""
    http_status = Http_status()
    return_data = {}
    
    try:
        #Récuperation du projet a affichier et des droits
        projet = recuperer_projet(slug,request.user,http_status)

        if request.method == 'POST' and request.is_ajax():
            form = Contact_ListeForm(request.POST)
            if form.is_valid():
                #TODO : Ajouter la gestion d'erreur lors d'un formulaire non valide
                #       (a voir dans quel ca ça arrive)
                contact_liste, created = Contact_Liste.objects.update_or_create(
                    projet=projet,
                    defaults={'projet':projet,'texte':form.save(commit=False).texte}
                )
                return_data.update({
                    'success': True,
                    'date_update': contact_liste.date_update.strftime('%Y-%m-%d %H:%M')
                })
                return JsonResponse(return_data)
        else:
            raise_SuspiciousOperation(http_status)        
    except Exception as ex:
        #Retourne l'erreur sous la forme d'une page ou d'un dico json
        return afficher_erreur(request,ex,http_status)
    return HttpResponseForbidden()
    
    
@login_required
def afficher_derniers_projets(request):
    """ Afficher les derniers projets du user."""
    http_status = Http_status()
    return_data = {}

    try:
        if request.method == 'GET':
            projet = Projet.objects.filter(createur=request.user).order_by('-date_update')#[:8]
            return_data = {'derniers_projets': projet}
            return render(request, 'projets/accueil.html', return_data)
        else:
            raise_SuspiciousOperation(http_status)
    except Exception as ex:
        #Retourne l'erreur sous la forme d'une page ou d'un dico json
        return afficher_erreur(request,ex,http_status)
    return HttpResponseForbidden()
