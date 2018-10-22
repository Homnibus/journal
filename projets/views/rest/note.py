from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from ...commun.error import Http_status, afficher_erreur, raise_SuspiciousOperation
from ...commun.utils import java_string_hashcode, JsonResponseContainer
from ...forms import Journal_EntreeForm
from ...models import Journal_Entree, get_current_timestamp, Projet


def is_authorized_to_create_note(user, codex):
    """
    Indicate if the user is authorized to create the note
    """
    if user == codex.createur:
        return True
    return False


def is_authorized_to_update_note(user, note):
    """
    Indicate if the user is authorized to update the note
    """
    if user == note.projet.createur:
        return True
    return False


def is_authorized_to_delete_note(user, note_id):
    """
    Indicate if the user is authorized to delete the note
    """
    # Get the task from the database
    note = Journal_Entree.objects.get(id=note_id)
    if user == note.projet.createur:
        return True
    return False


def post_note(request, codex_slug):
    """
    Create a new note of the day.
    """
    # Initialize the output data
    response = JsonResponseContainer()

    # Get the form
    form = Journal_EntreeForm(request.POST)

    # If the form is not valid, throw an error
    if not form.is_valid():
        # TODO: review the form validation
        form_errors = "form validation error"
        response.data.update({
            'success': False,
            'form_errors': form_errors
        })
        response.status = 400
        return response

    # Get the codex of the task from the slug
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
        return response

    # Check if a note already exist for today
    today = get_current_timestamp()
    note = Journal_Entree.objects.filter(
        projet=codex,
        date_creation__year=today.year,
        date_creation__month=today.month,
        date_creation__day=today.day
    ).first()

    # If a note was already created today, throw an error
    if note is not None:
        local_error = "Une note existe déjà pour ce jour"
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 400
        return response

    # Check if the user has the permission
    if not is_authorized_to_create_note(request.user, codex):
        local_error = "L'utilisateur n'est pas authorisé à créer cette note"
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 403
        return response

    # If all the above test are ok, create the note
    request_text = form.save(commit=False).texte
    note = Journal_Entree(projet=codex, texte=request_text)
    note.save()

    # Prepare the output data
    response.data.update({
        'success': True,
        'id': note.id
    })
    return response


def put_note(request):
    """
    Update the given note.
    """
    # Initialize the output data
    response = JsonResponseContainer()

    # Get the form
    form = Journal_EntreeForm(request.PUT)

    # Get the note id from the request
    note_id = request.PUT.get('id')

    # Get the note hash from the request
    request_note_hash = request.PUT.get('hash')

    # If the form is not valid, throw an error
    if not form.is_valid():
        # TODO : review the validation of the form
        form_errors = "form validation error"
        response.data.update({
            'success': False,
            'id': note_id,
            'form_errors': form_errors
        })
        response.status = 400
        return response

    # Get the text from the form
    request_text = form.save(commit=False).texte

    # Get the note from the database
    try:
        note = Journal_Entree.objects.get(id=note_id)
    except ObjectDoesNotExist:
        local_error = "La note n'existe pas."
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 404
        return response

    # If the note hash of the request doesn't correspond to the note hash of the database, throw an error
    database_note_hash = str(java_string_hashcode(note.texte))
    if request_note_hash != database_note_hash:
        local_error = "Cette page a été modifiée depuis la tentative de mise à jour."
        response.data.update({
            'success': False,
            'id': note_id,
            'local_error': local_error
        })
        response.status = 400
        return response

    # Check if the user has the permission
    if not is_authorized_to_update_note(request.user, note):
        local_error = "L'utilisateur n'est pas authorisé à modifier cette note"
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 403
        return response

    # If all the above test are ok, update the note
    note.texte = request_text
    note.save()

    # Prepare the output data
    response.data.update({
        'success': True,
        'id': note.id
    })
    return response


def delete_note(request):
    """
    Delete the given note.
    """
    # Initialize the output data
    response = JsonResponseContainer()
    # Get the note id from the request
    try:
        note_id = request.DELETE.get("id")
    except ObjectDoesNotExist:
        local_error = "La note n'existe pas."
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 404
        return response

    # Check if the user has the permission
    if not is_authorized_to_delete_note(request.user, note_id):
        local_error = "L'utilisateur n'est pas authorisé à supprimer cette note"
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 403
        return response

    # Delete the note
    Journal_Entree.objects.get(id=note_id).delete()

    # Prepare the output data
    response.data.update({
        'success': True,
        'id': note_id
    })
    return response


@login_required
def rest_note(request, codex_slug):
    """
    REST like actions on a note.
    """
    # Create the output data
    http_status = Http_status()
    response = None

    try:
        if not request.is_ajax():
            raise_SuspiciousOperation(http_status)

        if request.method == 'POST':
            response = post_note(request, codex_slug)
        elif request.method == 'PUT':
            response = put_note(request)
        elif request.method == 'DELETE':
            response = delete_note(request)
        else:
            raise_SuspiciousOperation(http_status)

        # Return the output data
        return JsonResponse(response.data, status=response.status)
    except Exception as ex:
        # Return the error as a html page or as a JSON dictionary
        return afficher_erreur(request, ex, http_status)
