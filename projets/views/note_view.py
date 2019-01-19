from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext

from projets.commun.error import (
    HttpInvalidFormData,
    HttpForbidden,
    HttpMethodNotAllowed,
)
from projets.commun.utils import (
    java_string_hashcode,
    JsonResponseContainer,
    get_object_or_not_found,
)
from projets.forms import NoteForm
from projets.models import Note, get_current_timestamp, Codex, Page


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
    Create a new note_details_view of the day.
    """
    # Initialize the output data
    response = JsonResponseContainer()

    # Get the form
    input_form = NoteForm(request.POST)

    # If the form is not valid, throw an error
    if not input_form.is_valid():
        raise HttpInvalidFormData(
            form_errors=input_form.non_field_errors(),
            fields_error=input_form.errors.as_json(),
        )

    # Get the codex of from the slug
    codex_slug = request.POST.get("codex_slug")

    # If the codex_slug is empty, throw an error
    if not codex_slug:
        # TODO : as the codex slug is in the POST param, it should be in the form validation
        form_errors = gettext("Form validation error.")
        response.data.update({"success": False, "form_errors": form_errors})
        response.status = 400
        return response.get_json_response()

    # Get the codex of the note from the slug
    codex = get_object_or_not_found(Codex, slug=codex_slug)

    # Check if a note_details_view already exist for today
    # TODO: try to upgrade the way this check is down
    today = get_current_timestamp().date()
    page = Page.objects.filter(codex=codex, date=today).select_related("note").first()

    # If a note_details_view was already created today, throw an error
    if hasattr(page, "note"):
        raise HttpInvalidFormData(
            form_errors=gettext("A Note already exist for today for this Codex.")
        )

    # Check if the user has the permission
    if not is_authorized_to_create_note(request.user, codex):
        raise HttpForbidden

    # If all the above test are ok, create the note_details_view
    request_text = input_form.save(commit=False).text
    # TODO : use the form to save the note
    note = Note(text=request_text)
    note.save(codex=codex)

    # Prepare the output data
    response.data.update({"success": True, "id": note.id})
    return response.get_json_response()


def put_note(request, note_id):
    """
    Update the given note_details_view.
    """
    # Initialize the output data
    response = JsonResponseContainer()

    # Get the form
    input_form = NoteForm(request.PUT)

    # Get the note_details_view hash from the request
    request_note_hash = request.PUT.get("hash")

    # If the form is not valid, throw an error
    if not input_form.is_valid():
        raise HttpInvalidFormData(
            form_errors=input_form.non_field_errors(),
            fields_error=input_form.errors.as_json(),
        )

    # Get the text from the form
    request_text = input_form.save(commit=False).text

    # Get the note from the database
    note = get_object_or_not_found(Note, id=note_id)

    # If the note_details_view hash of the request doesn't correspond to the note_details_view hash of the database,
    #  throw an error
    database_note_hash = str(java_string_hashcode(note.text))
    if request_note_hash != database_note_hash:
        raise HttpInvalidFormData(
            form_errors=gettext(
                "The Note have been modified since the last modification attempt."
            )
        )

    # Check if the user has the permission
    if not is_authorized_to_update_note(request.user, note):
        raise HttpForbidden

    # If all the above test are ok, update the note_details_view
    # TODO : use the form to save the note
    note.text = request_text
    note.save()

    # Prepare the output data
    response.data.update({"success": True})
    return response.get_json_response()


def delete_note(request, note_id):
    """
    Delete the given note_details_view.
    """
    # Initialize the output data
    response = JsonResponseContainer()

    # Check if the user has the permission
    if not is_authorized_to_delete_note(request.user, note_id):
        raise HttpForbidden

    # Get the note from the database
    note = get_object_or_not_found(Note, id=note_id)

    # Delete the note
    # TODO : add a test if the not does not exist
    # TODO : check if other delete use the same pattern (get the Model THEN delete it)
    note.delete()

    # Prepare the output data
    response.data.update({"success": True, "id": note_id})
    return response.get_json_response()


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
