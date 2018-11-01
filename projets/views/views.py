import logging

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..commun.codex import get_codex_from_slug
from ..commun.error import HttpStatus, render_error, raise_suspicious_operation
from ..forms import (TODO_EntreeForm)
from ..models import TODO_Entree, Task
from ..serializers import TaskSerializer

# Get an instance of a logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Tache:
    def __init__(self,model):
        self.form = None
        self.model = model
    
@login_required
@never_cache
def afficher_taches(request,slug,page_number=1):
    """Affiche la liste des taches d'un codex"""
    http_status = HttpStatus()
    return_data = {}
    
    try:
        #Récuperation du codex a affichier et des droits
        codex = get_codex_from_slug(slug, request.user, http_status)
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
            raise_suspicious_operation(http_status)
    except Exception as ex:
        #Retourne l'erreur sous la forme d'une page ou d'un dico json
        return render_error(request, ex, http_status)
    return HttpResponseForbidden()

    
        
@login_required
@never_cache
def afficher_taches_toutes(request,page_number=1,sort_by=None,sort_way=None):
    """Affiche la liste des taches de tout les codex"""
    http_status = HttpStatus()
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
            raise_suspicious_operation(http_status)
    except Exception as ex:
        #Retourne l'erreur sous la forme d'une page ou d'un dico json
        return render_error(request, ex, http_status)
    return HttpResponseForbidden()


@api_view(['GET', 'POST'])
def task_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Task.objects.all()
        serializer = TaskSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

