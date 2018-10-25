from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from projets.commun.error import HttpStatus, render_error, raise_suspicious_operation
from projets.commun.utils import java_string_hashcode, JsonResponseContainer
from projets.forms import Journal_EntreeForm
from projets.models import Journal_Entree, get_current_timestamp, Projet


def is_authorized_to_create_note(user, codex):
    """
    Indicate if the user is authorized to create the note_view
    """
    if user == codex.createur:
        return True
    return False


def is_authorized_to_update_note(user, note):
    """
    Indicate if the user is authorized to update the note_view
    """
    if user == note.projet.createur:
        return True
    return False


def is_authorized_to_delete_note(user, note_id):
    """
    Indicate if the user is authorized to delete the note_view
    """
    # Get the task_view from the database
    note = Journal_Entree.objects.get(id=note_id)
    if user == note.projet.createur:
        return True
    return False


def post_note(request, codex_slug):
    """
    Create a new note_view of the day.
    """
    # Initialize the output data
    response = JsonResponseContainer()

    # Get the form
    input_form = Journal_EntreeForm(request.POST)

    # If the form is not valid, throw an error
    if not input_form.is_valid():
        # TODO: review the form validation
        form_errors = "form validation error"
        response.data.update({
            'success': False,
            'form_errors': form_errors
        })
        response.status = 400
        return response.get_json_response()

    # Get the codex of the task_view from the slug
    try:
        codex = Projet.objects.get(slug=codex_slug)
    except ObjectDoesNotExist:
        # TODO : factorise this
        local_error = "Le codex n'existe pas."
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 404
        return response.get_json_response()

    # Check if a note_view already exist for today
    today = get_current_timestamp()
    note = Journal_Entree.objects.filter(
        projet=codex,
        date_creation__year=today.year,
        date_creation__month=today.month,
        date_creation__day=today.day
    ).first()

    # If a note_view was already created today, throw an error
    if note is not None:
        local_error = "Une note_view existe déjà pour ce jour"
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 400
        return response.get_json_response()

    # Check if the user has the permission
    if not is_authorized_to_create_note(request.user, codex):
        local_error = "L'utilisateur n'est pas authorisé à créer cette note_view"
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 403
        return response.get_json_response()

    # If all the above test are ok, create the note_view
    request_text = input_form.save(commit=False).texte
    note = Journal_Entree(projet=codex, texte=request_text)
    note.save()

    # Prepare the output data
    response.data.update({
        'success': True,
        'id': note.id
    })
    return response.get_json_response()


def put_note(request):
    """
    Update the given note_view.
    """
    # Initialize the output data
    response = JsonResponseContainer()

    # Get the form
    input_form = Journal_EntreeForm(request.PUT)

    # Get the note_view id from the request
    note_id = request.PUT.get('id')

    # Get the note_view hash from the request
    request_note_hash = request.PUT.get('hash')

    # If the form is not valid, throw an error
    if not input_form.is_valid():
        # TODO : review the validation of the form
        form_errors = "form validation error"
        response.data.update({
            'success': False,
            'id': note_id,
            'form_errors': form_errors
        })
        response.status = 400
        return response.get_json_response()

    # Get the text from the form
    request_text = input_form.save(commit=False).texte

    # Get the note_view from the database
    try:
        note = Journal_Entree.objects.get(id=note_id)
    except ObjectDoesNotExist:
        local_error = "La note_view n'existe pas."
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 404
        return response.get_json_response()

    # If the note_view hash of the request doesn't correspond to the note_view hash of the database, throw an error
    database_note_hash = str(java_string_hashcode(note.texte))
    if request_note_hash != database_note_hash:
        local_error = "Cette page a été modifiée depuis la tentative de mise à jour."
        response.data.update({
            'success': False,
            'id': note_id,
            'local_error': local_error
        })
        response.status = 400
        return response.get_json_response()

    # Check if the user has the permission
    if not is_authorized_to_update_note(request.user, note):
        local_error = "L'utilisateur n'est pas authorisé à modifier cette note_view"
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 403
        return response.get_json_response()

    # If all the above test are ok, update the note_view
    note.texte = request_text
    note.save()

    # Prepare the output data
    response.data.update({
        'success': True,
        'id': note.id
    })
    return response.get_json_response()


def delete_note(request):
    """
    Delete the given note_view.
    """
    # Initialize the output data
    response = JsonResponseContainer()
    # Get the note_view id from the request
    try:
        note_id = request.DELETE.get("id")
    except ObjectDoesNotExist:
        local_error = "La note_view n'existe pas."
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 404
        return response.get_json_response()

    # Check if the user has the permission
    if not is_authorized_to_delete_note(request.user, note_id):
        local_error = "L'utilisateur n'est pas authorisé à supprimer cette note_view"
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 403
        return response.get_json_response()

    # Delete the note_view
    Journal_Entree.objects.get(id=note_id).delete()

    # Prepare the output data
    response.data.update({
        'success': True,
        'id': note_id
    })
    return response.get_json_response()


@login_required
def note_view(request, codex_slug):
    """
    Manage REST like actions on a note_view.
    """
    # Create the output data
    http_status = HttpStatus()
    response = None

    try:
        if not request.is_ajax():
            raise_suspicious_operation(http_status)

        if request.method == 'POST':
            response = post_note(request, codex_slug)
        elif request.method == 'PUT':
            response = put_note(request)
        elif request.method == 'DELETE':
            response = delete_note(request)
        else:
            raise_suspicious_operation(http_status)

        # Return the output data
        return response
    except Exception as ex:
        # Return the error as a html page or as a JSON dictionary
        return render_error(request, ex, http_status)
