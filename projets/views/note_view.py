from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from projets.commun.error import (
    HttpInvalidFormData,
    HttpForbidden,
    HttpMethodNotAllowed,
)
from projets.commun.utils import get_object_or_not_found
from projets.forms import NoteUpdateForm, NoteCreateFromSlugForm
from projets.models import Note


def is_authorized_to_create_note(user, codex):
    """
    Indicate if the user is authorized to create the note_details_view
    """
    if user == codex.author:
        return True
    return False


def is_authorized_to_update_note(user, note):
    """
    Indicate if the user is authorized to update the note_details_view
    """
    if user == note.page.codex.author:
        return True
    return False


def is_authorized_to_delete_note(user, note_id):
    """
    Indicate if the user is authorized to delete the note_details_view
    """
    # Get the task_details_view from the database
    note = Note.objects.get(id=note_id)
    if user == note.page.codex.author:
        return True
    return False


def post_note(request):
    """
    Create a new note of the day.
    """
    # Get the form
    input_form = NoteCreateFromSlugForm(request.POST)

    # If the form is not valid, throw an error
    if not input_form.is_valid():
        raise HttpInvalidFormData(
            form_errors=input_form.non_field_errors(),
            fields_error=input_form.errors.as_json(),
        )

    # Check if the user has the permission
    # TODO : put the authorization check in the form or in the model save
    note = input_form.save(commit=False)
    if not is_authorized_to_create_note(request.user, note.page.codex):
        raise HttpForbidden

    # If all the above test are ok, create the note
    note = input_form.save()

    return JsonResponse({"success": True, "id": note.id})


def put_note(request, note_id):
    """
    Update the given note_details_view.
    """
    # Get the form
    input_data = request.PUT.copy()
    input_data.update({"id": note_id})
    input_form = NoteUpdateForm(input_data)

    # If the form is not valid, throw an error
    if not input_form.is_valid():
        raise HttpInvalidFormData(
            form_errors=input_form.non_field_errors(),
            fields_error=input_form.errors.as_json(),
        )

    # Check if the user has the permission
    # TODO : put the authorization check in the form or in the model save
    note = input_form.save(commit=False)
    if not is_authorized_to_update_note(request.user, note):
        raise HttpForbidden

    # If all the above test are ok, update the note
    input_form.save()

    return JsonResponse({"success": True})


def delete_note(request, note_id):
    """
    Delete the given note_details_view.
    """
    # Check if the user has the permission
    if not is_authorized_to_delete_note(request.user, note_id):
        raise HttpForbidden

    # Get the note from the database
    note = get_object_or_not_found(Note, id=note_id)

    # Delete the note
    note.delete()

    return JsonResponse({"success": True})


@login_required
def note_details_view(request, note_id):
    """
    Manage REST like actions on a note.
    """
    if request.method == "PUT" and request.is_ajax():
        response = put_note(request, note_id)
    elif request.method == "DELETE" and request.is_ajax():
        response = delete_note(request, note_id)
    else:
        raise HttpMethodNotAllowed

    # Return the output data
    return response


@login_required
def note_list_view(request):
    """
    Manage REST like actions on notes.
    """
    if request.method == "POST" and request.is_ajax():
        response = post_note(request)
    else:
        raise HttpMethodNotAllowed

    # Return the output data
    return response
