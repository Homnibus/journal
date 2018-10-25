from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from projets.commun.error import HttpStatus, raise_suspicious_operation, render_error
from projets.commun.utils import JsonResponseContainer
from projets.forms import Main_CouranteForm
from projets.models import Main_Courante, Projet


def get_codex_info(request, codex_slug, http_status):
    """
    Return the page of the information of the given codex
    """

    # Get the codex from the slug
    try:
        codex = Projet.objects.get(slug=codex_slug)
    except ObjectDoesNotExist:
        # TODO : factorise this
        http_status.status = 404
        http_status.message = "Le codex n'existe pas."
        http_status.explanation = "Le codex que vous voulez accéder n'existe pas."
        raise

    # Get the corresponding info
    codex_info = Main_Courante.objects.filter(projet=codex).first()

    # Create the output form
    form = Main_CouranteForm(instance=codex_info)

    return render(request, 'projets/codex_info.html', {'codex': codex, 'form': form, 'main_courante': codex_info})


def post_codex_info(request, codex_slug):
    """
    Update the information of the given codex
    """
    # Initialize the output data
    response = JsonResponseContainer()

    # Get the codex from the slug
    try:
        codex = Projet.objects.get(slug=codex_slug)
    except ObjectDoesNotExist:
        local_error = "Le codex n'existe pas."
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 404
        return response.get_json_response()

    # Get the form
    input_form = Main_CouranteForm(request.POST)

    # If the form is not valid, return an error status
    if not input_form.is_valid():
        # TODO : review the validation of the form
        form_errors = "form validation error"
        response.data.update({
            'success': False,
            'form_errors': form_errors
        })
        response.status = 400
        return response.get_json_response()

    # Update or create the codex info
    codex_info, created = Main_Courante.objects.update_or_create(
        projet=codex,
        defaults={'projet': codex, 'texte': input_form.save(commit=False).texte}
    )
    response.data.update({
        'success': True,
        'date_update': codex_info.date_update.strftime('%Y-%m-%d %H:%M')
    })
    return response.get_json_response()


@login_required
@never_cache
def codex_info_view(request, codex_slug):
    """
    Manage the codex information
    """
    # Initialize output
    response = None
    http_status = HttpStatus()

    try:
        if request.method == 'GET':
            response = get_codex_info(request, codex_slug, http_status)
        elif request.method == 'POST' and request.is_ajax():
            response = post_codex_info(request, codex_slug)
        else:
            raise_suspicious_operation(http_status)
        return response

    except Exception as ex:
        # Return the error as a html page or as a JSON dictionary
        return render_error(request, ex, http_status)
