from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext
from django.views.decorators.cache import never_cache

from projets.commun.error import HttpStatus, raise_suspicious_operation, render_error
from projets.commun.utils import JsonResponseContainer
from projets.forms import InformationForm
from projets.models import Information, Codex


def get_information(request, codex_slug, http_status):
    """
    Return the page of the information of the given codex
    """
    # Create the output date
    output_data = {}

    # Get the codex from the slug
    try:
        codex = Codex.objects.get(slug=codex_slug)
    except Codex.DoesNotExist:
        # TODO : factorise this
        http_status.status = 404
        http_status.message = gettext("The Codex does not exist.")
        http_status.explanation = gettext(
            "The codex you are trying to access does not exist."
        )
        raise

    # Get the corresponding information
    codex_information = Information.objects.filter(codex=codex).first()

    # Create the output form
    form = InformationForm(instance=codex_information)

    # Update the output data
    output_data.update({"codex": codex, "form": form, "information": codex_information})

    return render(request, "projets/information.html", output_data)


def post_information(request, codex_slug):
    """
    Update the information of the given codex
    """
    # Initialize the output data
    response = JsonResponseContainer()

    # Get the codex from the slug
    try:
        codex = Codex.objects.get(slug=codex_slug)
    except Codex.DoesNotExist:
        local_error = gettext("The Codex does not exist")
        response.data.update({"success": False, "local_error": local_error})
        response.status = 404
        return response.get_json_response()

    # Get the form
    input_form = InformationForm(request.POST)

    # If the form is not valid, return an error status
    if not input_form.is_valid():
        # TODO : review the validation of the form
        form_errors = gettext("Form validation error.")
        response.data.update({"success": False, "form_errors": form_errors})
        response.status = 400
        return response.get_json_response()

    # Update or create the codex info
    input_form.save(codex=codex)

    response.data.update({"success": True})
    return response.get_json_response()


@login_required
@never_cache
def information_view(request, codex_slug):
    """
    Manage the codex information
    """
    # Initialize output
    response = None
    http_status = HttpStatus()

    try:
        if request.method == "GET":
            response = get_information(request, codex_slug, http_status)
        elif request.method == "POST" and request.is_ajax():
            response = post_information(request, codex_slug)
        else:
            raise_suspicious_operation(http_status)
        return response

    except Exception as ex:
        # Return the error as a html page or as a JSON dictionary
        return render_error(request, ex, http_status)
