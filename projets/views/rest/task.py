from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from ...commun.error import Http_status, afficher_erreur, raise_SuspiciousOperation
from ...commun.utils import java_string_hashcode, JsonResponseContainer
from ...forms import TODO_EntreeForm
from ...models import TODO_Entree, Projet


def is_authorized_to_create_task(user, codex):
    """
    Indicate if the user is authorized to create the task
    """
    if user == codex.createur:
        return True
    return False


def is_authorized_to_update_task(user, task):
    """
    Indicate if the user is authorized to update the task
    """
    if user == task.projet.createur:
        return True
    return False


def is_authorized_to_delete_task(user, task_id):
    """
    Indicate if the user is authorized to delete the task
    """
    # Get the task from the database
    task = TODO_Entree.objects.get(id=task_id)
    if user == task.projet.createur:
        return True
    return False


def post_task(request, codex_slug):
    """
    Create a new task for the given codex.
    """
    # Initialize the output data
    response = JsonResponseContainer()

    # Get the form
    form = TODO_EntreeForm(request.POST)

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

    # Get the task model from the form
    form_task = form.save(commit=False)

    # If the task text is empty, throw an error
    if not form_task.texte or form_task.texte.isspace():
        local_error = "Impossible de créer une tache vide"
        response.data.update({
            'success': False,
            'local_error': local_error
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

    # Check if the user has the permission
    if not is_authorized_to_create_task(request.user, codex):
        local_error = "L'utilisateur n'est pas authorisé à créer cette tache"
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 403
        return response

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
    response.data.update({
        'success': True,
        'out_form': output_form,
        'id': task.id
    })
    return response


def put_task(request):
    """
    Update the given task
    """
    # Initialize the output data
    response = JsonResponseContainer()

    # Get the form
    form = TODO_EntreeForm(request.PUT)

    # Get the task id from the request
    task_id = request.PUT.get('id')

    # Get the task hash from the request
    request_task_hash = request.PUT.get('hash')

    # If the form is not valid, throw an error
    if not form.is_valid():
        # TODO : review the validation of the form
        form_errors = "form validation error"
        response.data.update({
            'success': False,
            'id': task_id,
            'form_errors': form_errors
        })
        response.status = 400
        return response

    # Get the task model from the form
    form_task = form.save(commit=False)

    # Get the task from the database
    try:
        task = TODO_Entree.objects.get(id=task_id)
    except ObjectDoesNotExist:
        local_error = "La tache que vous voulez modifier n'existe pas."
        response.data.update({
            'success': False,
            'id': task_id,
            'local_error': local_error
        })
        response.status = 404
        return response

    # If the task hash of the request doesn't correspond to the task hash of the database, throw an error
    database_task_hash = str(java_string_hashcode(task.texte))
    if request_task_hash != database_task_hash:
        local_error = "Cette page a été modifié depuis la tentative de mise à jour."
        response.data.update({
            'success': False,
            'id': task_id,
            'local_error': local_error
        })
        response.status = 400
        return response

    # Check if the user has the permission
    if not is_authorized_to_update_task(request.user, task):
        local_error = "L'utilisateur n'est pas authorisé à modifier cette tache"
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 403
        return response

    # If all the above test are ok, update the task
    task.texte = form_task.texte
    task.realisee = form_task.realisee
    task.save()

    # Prepare the output data
    response.data.update({
        'success': True,
        'id': task.id
    })
    return response


def delete_task(request):
    """
    Delete the given note.
    """
    # Initialize the output data
    response = JsonResponseContainer()

    # Get the task id from the request
    try:
        task_id = request.DELETE.get("id")
    except ObjectDoesNotExist:
        local_error = "La tache que vous voulez supprimer n'existe pas."
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 404
        return response

    # Check if the user has the permission
    if not is_authorized_to_delete_task(request.user, task_id):
        local_error = "L'utilisateur n'est pas authorisé à supprimer cette tache"
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 403
        return response

    # Delete the task
    TODO_Entree.objects.filter(id=task_id).delete()

    # Prepare the output data
    response.data.update({
        'success': True,
        'id': task_id
    })
    return response


@login_required
def rest_task(request, slug):
    """
    REST like actions on a task.
    """
    # Create the output data
    http_status = Http_status()
    response = None

    try:
        if not request.is_ajax():
            raise_SuspiciousOperation(http_status)

        if request.method == 'POST':
            response = post_task(request, slug)
        elif request.method == 'PUT':
            response = put_task(request)
        elif request.method == 'DELETE':
            response = delete_task(request)
        else:
            raise_SuspiciousOperation(http_status)

        # Return the output data
        return JsonResponse(response.data, status=response.status)
    except Exception as ex:
        # Return the error as a html page or as a JSON dictionary
        return afficher_erreur(request, ex, http_status)
