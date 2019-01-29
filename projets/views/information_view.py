from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from projets.commun.error import (
    HttpInvalidFormData,
    HttpMethodNotAllowed,
    HttpForbidden,
    HttpConflict,
)
from projets.commun.utils import get_object_or_not_found, java_string_hashcode
from projets.forms import InformationCreateForm, InformationUpdateForm
from projets.models import Information, Codex


def is_authorized_to_create_information(user, codex):
    """
    Return True if the user is authorized to create the information.
    """
    if user == codex.author:
        return True
    return False


def is_authorized_to_update_information(user, information):
    """
    Return True if the user is authorized to update the information.
    """
    if user == information.codex.author:
        return True
    return False


def is_authorized_to_get_information(user, codex):
    """
    Return True if the user is authorized to get the information.
    """
    if user == codex.author:
        return True
    return False


def get_information(request, codex):
    """
    Return the information for the given codex.
    """
    # Check if the user has the permission to perform the action
    if not is_authorized_to_get_information(request.user, codex):
        raise HttpForbidden

    # Initialise the django representation of a form with the input data
    information = Information.objects.filter(codex=codex).first()
    form = InformationUpdateForm(instance=information)

    return render(
        request,
        "projets/information.html",
        {"codex": codex, "form": form, "information": information},
    )


def post_information(request, codex):
    """
    Create the information of the given codex
    """
    # Check if the user has the permission to perform the action
    if not is_authorized_to_create_information(request.user, codex):
        raise HttpForbidden

    # Initialise the django representation of a form with the input data
    input_form = InformationCreateForm(data=request.POST, codex=codex)

    # Check if the input data are valid
    if not input_form.is_valid():
        raise HttpInvalidFormData(
            form_errors=input_form.non_field_errors(),
            fields_error=input_form.errors,
        )

    # Create the information
    try:
        information = input_form.save(codex=codex)
    except IntegrityError:
        raise HttpConflict(Information._meta.model_name)

    # Get the created information hash to return it
    information_hash = java_string_hashcode(information.text)

    return JsonResponse(
        {"success": True, "hash": information_hash, "id": information.id}
    )


def put_information(request, information):
    """
    Update the information of the given codex.
    """
    # Check if the user has the permission to perform the action
    if not is_authorized_to_update_information(request.user, information):
        raise HttpForbidden

    # Initialise the django representation of a form with the input data
    input_form = InformationUpdateForm(request.PUT, instance=information)

    # If the form is not valid, return an error status
    if not input_form.is_valid():
        raise HttpInvalidFormData(
            form_errors=input_form.non_field_errors(),
            fields_error=input_form.errors,
        )

    # Update the information
    input_form.save()

    return JsonResponse({"success": True})


@login_required
def information_details_view(request, codex_slug):
    """
    Manage the update of a codex information.
    """
    # Check if the requested resource exist
    codex = get_object_or_not_found(Codex, slug=codex_slug)
    information = get_object_or_not_found(Information, codex=codex)

    # Rout the request according to the asked method
    if request.method == "PUT" and request.is_ajax():
        response = put_information(request, information)
    else:
        raise HttpMethodNotAllowed
    return response


@login_required
@never_cache
def information_list_view(request, codex_slug):
    """
    Manage the creation and listing of a codex information.
    """
    # Check if the requested resource exist
    codex = get_object_or_not_found(Codex, slug=codex_slug)

    # Rout the request according to the asked method
    if request.method == "GET" and not request.is_ajax():
        response = get_information(request, codex)
    elif request.method == "POST" and request.is_ajax():
        response = post_information(request, codex)
    else:
        raise HttpMethodNotAllowed
    return response
