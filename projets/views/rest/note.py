from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from ...commun.codex import get_codex_from_slug
from ...commun.error import Http_status, afficher_erreur, raise_SuspiciousOperation
from ...commun.utils import java_string_hashcode
from ...forms import Journal_EntreeForm
from ...models import Journal_Entree, get_current_timestamp


def post_note(request, codex_slug, http_status):
    """
    Create a new note of the day.
    """
    # Create the output data
    output_data = {}
    try:
        # Get the form
        form = Journal_EntreeForm(request.POST)

        # If the form is not valid, throw an error
        if not form.is_valid():
            form_errors = str(form.non_field_errors) + str(form.texte.errors)
            output_data.update({
                'success': False,
                'form_errors': form_errors
            })
            return output_data
        # Get the codex of the note from the slug
        codex = get_codex_from_slug(codex_slug, request.user, http_status)

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
            http_status.status = 404
            http_status.message = "La page du jours existe déjà."
            http_status.explanation = "La page que vous voulez créer existe déjà."
            return output_data

        # If all the above test are ok, create the note
        request_text = form.save(commit=False).texte
        note = Journal_Entree(projet=codex, texte=request_text)
        note.save()

        # Prepare the output data
        output_data.update({
            'success': True,
            'id': note.id
        })
        return output_data

    except Exception:
        raise


def put_note(request, http_status):
    """
    Update the given note.
    """
    # Create the output data
    output_data = {}
    try:
        # Get the form
        form = Journal_EntreeForm(request.PUT)

        # Get the note id from the request
        note_id = request.PUT.get('id')

        # Get the note hash from the request
        request_note_hash = request.PUT.get('hash')

        # If the form is not valid, throw an error
        if not form.is_valid():
            form_errors = str(form.non_field_errors) + str(form.texte.errors)
            output_data.update({
                'success': False,
                'id': note_id,
                'form_errors': form_errors
            })
            return output_data

        # Get the text from the form
        request_text = form.save(commit=False).texte

        # Get the note from the database
        note = Journal_Entree.objects.get(id=note_id)

        # If the note hash of the request doesn't correspond to the note hash of the database, throw an error
        database_note_hash = str(java_string_hashcode(note.texte))
        if request_note_hash != database_note_hash:
            local_error = "Cette page a été modifiée depuis la tentative de mise à jour."
            output_data.update({
                'success': False,
                'id': note_id,
                'local_error': local_error
            })
            return output_data

        # If all the above test are ok, update the note
        note.texte = request_text
        note.save()

        # Prepare the output data
        output_data.update({
            'success': True,
            'id': note.id
        })
        return output_data

    except ObjectDoesNotExist:
        http_status.status = 404
        http_status.message = "L'entree de journal n'existe pas."
        http_status.explanation = "L'entree de journal que vous voulez accéder n'existe pas."
        raise
    except Exception:
        raise


def delete_note(request, http_status):
    """
    Delete the given note.
    """
    # Create the output data
    output_data = {}
    try:
        # Get the note id from the request
        note_id = request.DELETE.get("id")

        # Delete the note
        Journal_Entree.objects.get(id=note_id).delete()

        # Prepare the output data
        output_data.update({
            'success': True,
            'id': note_id
        })
        return output_data

    except ObjectDoesNotExist:
        http_status.status = 404
        http_status.message = "L'entree de journal n'existe pas."
        http_status.explanation = "L'entree de journal que vous voulez supprimer n'existe pas."
        raise
    except Exception:
        raise


@login_required
def rest_note(request, codex_slug):
    """
    REST like actions on a note.
    """
    # Create the output data
    http_status = Http_status()
    output_data = {}

    try:
        if not request.is_ajax():
            raise_SuspiciousOperation(http_status)

        if request.method == 'POST':
            output_data = post_note(request, codex_slug, http_status)
        elif request.method == 'PUT':
            output_data = put_note(request, http_status)
        elif request.method == 'DELETE':
            output_data = delete_note(request, http_status)
        else:
            raise_SuspiciousOperation(http_status)

        # Return the output data
        return JsonResponse(output_data)
    except Exception as ex:
        # Return the error as a html page or as a JSON dictionary
        return afficher_erreur(request, ex, http_status)
