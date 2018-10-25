from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projets.commun.error import HttpStatus, raise_suspicious_operation, render_error
from projets.models import Projet


def get_recent_codex(request):
    """
    Return the recent codex page
    """
    # Initialize output
    output_data = {}

    # Get all the codex
    codex = Projet.objects.filter(createur=request.user).order_by('-date_update')

    # Add the codex to the output data
    output_data.update({'derniers_codex': codex})

    return render(request, 'projets/accueil.html', output_data)


@login_required
def recent_codex_view(request):
    """
    Manage the recent codex view
    """
    # Initialize output
    http_status = HttpStatus()
    response = None

    try:
        if request.method == 'GET':
            response = get_recent_codex(request)
        else:
            raise_suspicious_operation(http_status)
        return response

    except Exception as ex:
        # Return the error as a html page or as a JSON dictionary
        return render_error(request, ex, http_status)
