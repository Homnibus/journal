from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from projets.commun.error import HttpInvalidFormData, HttpMethodNotAllowed
from projets.commun.utils import JsonResponseContainer, get_object_or_not_found
from projets.forms import InformationForm
from projets.models import Information, Codex


def get_information(request, codex_slug):
    """
    Return the page of the information of the given codex
    """
    # Create the output date
    output_data = {}

    # Get the codex from the slug
    codex = get_object_or_not_found(Codex, slug=codex_slug)

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
    codex = get_object_or_not_found(Codex, slug=codex_slug)

    # Get the form
    input_form = InformationForm(request.POST)

    # If the form is not valid, return an error status
    if not input_form.is_valid():
        raise HttpInvalidFormData(
            form_errors=input_form.non_field_errors(),
            fields_error=input_form.errors.as_json(),
        )

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
    if request.method == "GET" and not request.is_ajax():
        response = get_information(request, codex_slug)
    elif request.method == "POST" and request.is_ajax():
        response = post_information(request, codex_slug)
    else:
        raise HttpMethodNotAllowed
    return response
