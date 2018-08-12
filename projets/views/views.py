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
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache

from ..models import Projet, Main_Courante, Journal_Entree, TODO_Entree, get_current_timestamp
from ..forms import (ProjetForm, Main_CouranteForm, Journal_EntreeForm, TODO_EntreeForm)
from ..commun.error import Http_status, afficher_erreur, raise_SuspiciousOperation
from ..commun.codex import recuperer_codex

# Get an instance of a logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
        
@login_required
@never_cache
def afficher_main_courante(request,slug):
    """ Afficher la main courante d'un codex."""
    http_status = Http_status()
    return_data = {}

    try:
        #Récuperation du codex a affichier et des droits
        codex = recuperer_codex(slug,request.user,http_status)

        if request.method == 'GET':
            main_courante = Main_Courante.objects.filter(projet=codex).first()
            form = Main_CouranteForm(instance=main_courante)
            return render(request, 'projets/codex_info.html', {'codex':codex,'form':form,'main_courante':main_courante})    
        else:
            raise_SuspiciousOperation(http_status)
    except Exception as ex:
        #Retourne l'erreur sous la forme d'une page ou d'un dico json
        return afficher_erreur(request,ex,http_status)
    return HttpResponseForbidden()

    
@login_required
def maj_main_courante(request,slug):
    """ Modifier la main courante d'un codex."""
    http_status = Http_status()
    return_data = {}
    
    try:
        #Récuperation du codex a affichier et des droits
        codex = recuperer_codex(slug,request.user,http_status)
        
        if request.method == 'POST' and request.is_ajax():
            form = Main_CouranteForm(request.POST)
            if form.is_valid():
                #TODO : Ajouter la gestion d'erreur lors d'un formulaire non
                #       valide (a voir dans quel ca ça arrive)
                main_courante, created = Main_Courante.objects.update_or_create(
                    projet=codex,
                    defaults={'projet':codex,'texte':form.save(commit=False).texte}
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
def afficher_derniers_codex(request):
    """ Afficher les derniers codexs du user."""
    http_status = Http_status()
    return_data = {}

    try:
        if request.method == 'GET':
            codex = Projet.objects.filter(createur=request.user).order_by('-date_update')#[:8]
            return_data.update({'derniers_codex': codex})
            return render(request, 'projets/accueil.html', return_data)
        else:
            raise_SuspiciousOperation(http_status)
    except Exception as ex:
        #Retourne l'erreur sous la forme d'une page ou d'un dico json
        return afficher_erreur(request,ex,http_status)
    return HttpResponseForbidden()

        
class Tache():
    def __init__(self,model):
        self.form = None
        self.model = model
    
@login_required
@never_cache
def afficher_taches(request,slug,page_number=1):
    """Affiche la liste des taches d'un codex"""
    http_status = Http_status()
    return_data = {}
    
    try:
        #Récuperation du codex a affichier et des droits
        codex = recuperer_codex(slug,request.user,http_status)
        return_data.update({'codex': codex})

        if request.method == 'GET':
            #Récupération de la liste des taches
            tache_model_liste = TODO_Entree.objects.filter(
                projet=codex,
            ).order_by('realisee','date_creation')
            #Creation d'une liste de formulaire
            tache_liste = []
            for model_courant in tache_model_liste:
                tache = Tache(model=model_courant)
                tache.form = TODO_EntreeForm(instance=model_courant)
                tache_liste.append(tache)
            #Creation de l'objet paginator
            paginator = Paginator(tache_liste,10)
            #Creation de la page
            try:
                page = paginator.page(page_number)
            #Si on est sur une page qui n'existe pas ou qui est vide, on retourne la dernière page par defaut
            except EmptyPage:
                page = paginator.page(paginator.num_pages)
            #Ajout de la page au resultat
            return_data.update({'task_list':page})
            #Creation du paginator_range pour pouvoir naviguer plus facilement 
            paginator_range = range(1,paginator.num_pages+1)
            #Ajout du range au resultat
            return_data.update({'paginator_range':paginator_range})
            
            return render(request, 'projets/codex_taches.html', return_data)
        else:
            raise_SuspiciousOperation(http_status)        
    except Exception as ex:
        #Retourne l'erreur sous la forme d'une page ou d'un dico json
        return afficher_erreur(request,ex,http_status)
    return HttpResponseForbidden()

    
        
@login_required
@never_cache
def afficher_taches_toutes(request,page_number=1,sort_by=None,sort_way=None):
    """Affiche la liste des taches de tout les codex"""
    http_status = Http_status()
    return_data = {}
    
    try:
        if request.method == 'GET':
            #Récupération de la liste des taches
            tache_model_liste = TODO_Entree.objects.select_related()
            #Trie de la liste
            sort_arg = []
            if sort_by in ['realisee','texte','projet__titre','date_realisee','date_creation']:
                if sort_way == 'desc':
                    sort_arg.append('-' + sort_by)
                else :    
                    sort_arg.append(sort_by)
            sort_arg.extend(['realisee','date_creation'])
            tache_model_liste = tache_model_liste.order_by(*sort_arg)
            #On passe les paramètres de trie à la vue
            return_data.update({'sort_by':sort_by,'sort_way':sort_way})
            #Creation d'une liste de formulaire
            tache_liste = []
            for model_courant in tache_model_liste:
                tache = Tache(model=model_courant)
                tache.form = TODO_EntreeForm(instance=model_courant)
                tache_liste.append(tache)
            #Creation de l'objet paginator
            paginator = Paginator(tache_liste,10)
            #Creation de la page
            try:
                page = paginator.page(page_number)
            #Si on est sur une page qui n'existe pas ou qui est vide, on retourne la dernière page par defaut
            except EmptyPage:
                page = paginator.page(paginator.num_pages)
            #Ajout de la page au resultat
            return_data.update({'task_list':page})
            #Creation du paginator_range pour pouvoir naviguer plus facilement 
            paginator_range = range(1,paginator.num_pages+1)
            #Ajout du range au resultat
            return_data.update({'paginator_range':paginator_range})
            return render(request, 'projets/codex_taches_toutes.html', return_data)
        else:
            raise_SuspiciousOperation(http_status)        
    except Exception as ex:
        #Retourne l'erreur sous la forme d'une page ou d'un dico json
        return afficher_erreur(request,ex,http_status)
    return HttpResponseForbidden()
