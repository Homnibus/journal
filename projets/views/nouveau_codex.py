from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.cache import never_cache

from ..forms import ProjetForm
from ..commun.error import Http_status, afficher_erreur, raise_SuspiciousOperation

@login_required
@never_cache
def creer_codex(request):
    """Affiche un codex pour creation."""
    http_status = Http_status()
    return_data = {}

    try:
        if request.method == 'GET' or request.method == 'POST':
            form = ProjetForm(request.POST or None)
            return_data.update({'form':form})
            if form.is_valid():
                codex = form.save(commit=False)
                codex.createur = request.user
                codex.save()
                return_data.update({'codex':codex})
                return redirect('afficher_codex', slug=codex.slug)
            return render( request, 'projets/nouveau_codex.html', return_data)
        else:
            raise_SuspiciousOperation(http_status)    
    except Exception as ex:
        #Retourne l'erreur sous la forme d'une page ou d'un dico json
        return afficher_erreur(request,ex,http_status)
    return HttpResponseForbidden()
        
