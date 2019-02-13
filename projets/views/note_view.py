from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse

from projets.commun.error import (
    HttpInvalidFormData,
    HttpForbidden,
    HttpMethodNotAllowed,
    HttpConflict,
)
from projets.commun.utils import get_object_or_not_found, java_string_hashcode
from projets.forms import NoteUpdateForm, NoteCreateForm, NoteDeleteForm
from projets.models import Note, Codex


def is_authorized_to_create_note(user, codex):
    """
    Return True if the user is authorized to create the note.
    """
    if user == codex.author:
        return True
    return False


def is_authorized_to_update_note(user, note):
    """
    Return True if the user is authorized to update the note.
    """
    if user == note.page.codex.author:
        return True
    return False


def is_authorized_to_delete_note(user, note):
    """
    Return True if the user is authorized to delete the note.
    """
    if user == note.page.codex.author:
        return True
    return False


def post_note(request, codex):
    """
    Create a new note for the given codex and for the current day.
    """
    # Check if the user has the permission to perform the action
    if not is_authorized_to_create_note(request.user, codex):
        raise HttpForbidden

    # Initialise the django representation of a form with the input data
    input_form = NoteCreateForm(data=request.POST, codex=codex)

    # Check if the input data are valid
    if not input_form.is_valid():
        raise HttpInvalidFormData(
            form_errors=input_form.non_field_errors(),
            fields_error=input_form.errors,
        )

    # Create the note
    try:
        note = input_form.save()
    except IntegrityError:
        raise HttpConflict(Note._meta.model_name)

    # Get the created note hash to return it
    note_hash = java_string_hashcode(note.text)

    return JsonResponse({"success": True, "id": note.id, "hash": note_hash})


def put_note(request, note):
    """
    Update the given note.
    """
    # Check if the user has the permission to perform the action
    if not is_authorized_to_update_note(request.user, note):
        raise HttpForbidden

    # Initialise the django representation of a form with the input data
    input_form = NoteUpdateForm(request.PUT, instance=note)

    # Check if the input data are valid
    if not input_form.is_valid():
        raise HttpInvalidFormData(
            form_errors=input_form.non_field_errors(),
            fields_error=input_form.errors,
        )

    # Update the note
    input_form.save()

    return JsonResponse({"success": True})


def delete_note(request, note):
    """
    Delete the given note.
    """
    # Check if the user has the permission to perform the action
    if not is_authorized_to_delete_note(request.user, note):
        raise HttpForbidden

    # Initialise the django representation of a form with the input data
    input_form = NoteDeleteForm(request.DELETE, instance=note)

    # Check if the input data are valid
    if not input_form.is_valid():
        raise HttpInvalidFormData(
            form_errors=input_form.non_field_errors(),
            fields_error=input_form.errors,
        )

    # Delete the note
    note.delete()

    return JsonResponse({"success": True})


@login_required
def note_details_view(request, note_id):
    """
    Manage the update and deletion of a note.
    """
    # Check if the requested resource exist
    note = get_object_or_not_found(Note, id=note_id)

    if request.method == "PUT" and request.is_ajax():
        response = put_note(request, note)
    elif request.method == "DELETE" and request.is_ajax():
        response = delete_note(request, note)
    else:
        raise HttpMethodNotAllowed

    return response


@login_required
def note_list_view(request, codex_slug):
    """
    Manage the creation of a note.
    """
    # Check if the requested resource exist
    codex = get_object_or_not_found(Codex, slug=codex_slug)

    if request.method == "POST" and request.is_ajax():
        response = post_note(request, codex)
    else:
        raise HttpMethodNotAllowed

    return response
