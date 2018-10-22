from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from ...commun.codex import get_codex_from_slug
from ...commun.error import Http_status, afficher_erreur, raise_SuspiciousOperation
from ...commun.utils import java_string_hashcode
from ...forms import TODO_EntreeForm
from ...models import TODO_Entree


def post_task(request, codex_slug, http_status):
    """
    Create a new task for the given codex.
    """
    # Create the output data
    output_data = {}
    try:
        # Get the form
        form = TODO_EntreeForm(request.POST)

        # If the form is not valid, throw an error
        if not form.is_valid():
            form_errors = str(form.non_field_errors) + str(form.texte.errors)
            output_data.update({
                'success': False,
                'form_errors': form_errors
            })
            return output_data

        # Get the task model from the form
        form_task = form.save(commit=False)

        # If the task text is empty, throw an error
        if not form_task.texte or form_task.texte.isspace():
            local_error = "Impossible de créer une tache vide"
            output_data.update({
                'success': False,
                'local_error': local_error
            })
            return output_data

        # Get the codex of the task from the slug
        codex = get_codex_from_slug(codex_slug, request.user, http_status)

        # If all the above test are ok, create the task
        task = TODO_Entree(
            projet=codex,
            texte=form_task.texte,
            realisee=form_task.realisee
        )
        task.save()

        # TODO : change the way this data is returned
        # Récupération du html d'un nouveau formulaire avec les données mises à jours pour affichage
        # et ajout aux données à retourner
        output_form = '<table>' + str(TODO_EntreeForm(instance=task)) + '</table>'

        # Prepare the output data
        output_data.update({
            'success': True,
            'out_form': output_form,
            'id': task.id
        })
        return output_data

    except Exception:
        raise


def put_task(request, http_status):
    """
    Update the given task
    """
    # Create the output data
    output_data = {}

    try:
        # Get the form
        form = TODO_EntreeForm(request.PUT)

        # Get the task id from the request
        task_id = request.PUT.get('id')

        # Get the task hash from the request
        request_task_hash = request.PUT.get('hash')

        # If the form is not valid, throw an error
        if not form.is_valid():
            form_errors = str(form.non_field_errors) + str(form.texte.errors)
            output_data.update({
                'success': False,
                'id': task_id,
                'form_errors': form_errors
            })
            return output_data

        # Get the task model from the form
        form_task = form.save(commit=False)

        # Get the task from the database
        task = TODO_Entree.objects.get(id=task_id)

        # If the task hash of the request doesn't correspond to the task hash of the database, throw an error
        database_task_hash = str(java_string_hashcode(task.texte))
        if request_task_hash != database_task_hash:
            local_error = "Cette page a été modifié depuis la tentative de mise à jour."
            output_data.update({
                'success': False,
                'id': task_id,
                'local_error': local_error
            })
            return output_data

        # If all the above test are ok, update the task
        task.texte = form_task.texte
        task.realisee = form_task.realisee
        task.save()

        # Prepare the output data
        output_data.update({
            'success': True,
            'id': task.id
        })
        return output_data

    except ObjectDoesNotExist:
        http_status.status = 404
        http_status.message = "La tache n'existe pas."
        http_status.explanation = "La tache que vous voulez mettre à jour n'existe pas."
        raise
    except Exception:
        raise


def delete_task(request, http_status):
    """
    Delete the given note.
    """
    # Create the output data
    output_data = {}

    try:
        # Get the task id from the request
        task_id = request.DELETE.get("id")

        # Delete the task
        TODO_Entree.objects.filter(id=task_id).delete()

        # Prepare the output data
        output_data.update({
            'success': True,
            'id': task_id
        })
        return output_data

    except ObjectDoesNotExist:
        http_status.status = 404
        http_status.message = "La tache n'existe pas."
        http_status.explanation = "La tache que vous voulez accéder n'existe pas."
        raise
    except Exception:
        raise


@login_required
def rest_task(request, slug):
    """
    REST like actions on a task.
    """
    # Create the output data
    http_status = Http_status()
    return_data = {}

    try:
        if not request.is_ajax():
            raise_SuspiciousOperation(http_status)

        if request.method == 'POST':
            return_data = post_task(request, slug, http_status)
        elif request.method == 'PUT':
            return_data = put_task(request, http_status)
        elif request.method == 'DELETE':
            return_data = delete_task(request, http_status)
        else:
            raise_SuspiciousOperation(http_status)

        # Return the output data
        return JsonResponse(return_data)
    except Exception as ex:
        # Return the error as a html page or as a JSON dictionary
        return afficher_erreur(request, ex, http_status)
