from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from projets.commun.error import HttpStatus, render_error, raise_suspicious_operation
from projets.commun.utils import java_string_hashcode, JsonResponseContainer
from projets.forms import TaskForm
from projets.models import Codex, Task


def is_authorized_to_create_task(user, codex):
    """
    Indicate if the user is authorized to create the task_view
    """
    if user == codex.author:
        return True
    return False


def is_authorized_to_update_task(user, task):
    """
    Indicate if the user is authorized to update the task_view
    """
    if user == task.page.codex.author:
        return True
    return False


def is_authorized_to_delete_task(user, task_id):
    """
    Indicate if the user is authorized to delete the task_view
    """
    # Get the task_view from the database
    task = Task.objects.get(id=task_id)
    if user == task.page.codex.author:
        return True
    return False


def post_task(request, codex_slug):
    """
    Create a new task_view for the given codex.
    """
    # Initialize the output data
    response = JsonResponseContainer()

    # Get the form
    input_form = TaskForm(request.POST)

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

    # Get the task_view model from the form
    form_task = input_form.save(commit=False)

    # TODO: put this test in the form validation
    # If the task_view text is empty, throw an error
    if not form_task.text or form_task.text.isspace():
        local_error = "Impossible de créer une tache vide"
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 400
        return response.get_json_response()

    # Get the codex of the task_view from the slug
    try:
        codex = Codex.objects.get(slug=codex_slug)
    except ObjectDoesNotExist:
        # TODO : factorise this
        local_error = "Le codex n'existe pas."
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 404
        return response.get_json_response()

    # Check if the user has the permission
    if not is_authorized_to_create_task(request.user, codex):
        local_error = "L'utilisateur n'est pas authorisé à créer cette tache"
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 403
        return response.get_json_response()

    # If all the above test are ok, create the task_view
    task = Task(
        text=form_task.text,
        is_achieved=form_task.is_achieved
    )
    task.save(codex=codex)

    # TODO : change the way this data is returned
    # Récupération du html d'un nouveau formulaire avec les données mises à jours pour affichage
    # et ajout aux données à retourner
    output_form = '<table>' + str(TaskForm(instance=task)) + '</table>'

    # Prepare the output data
    response.data.update({
        'success': True,
        'out_form': output_form,
        'id': task.id
    })
    return response.get_json_response()


def put_task(request):
    """
    Update the given task_view
    """
    # Initialize the output data
    response = JsonResponseContainer()

    # Get the form
    input_form = TaskForm(request.PUT)

    # TODO : get this information from the form
    # Get the task_view id from the request
    task_id = request.PUT.get('id')

    # TODO : get this information from the form
    # Get the task_view hash from the request
    request_task_hash = request.PUT.get('hash')

    # If the form is not valid, throw an error
    if not input_form.is_valid():
        # TODO : review the validation of the form
        form_errors = "form validation error"
        response.data.update({
            'success': False,
            'id': task_id,
            'form_errors': form_errors
        })
        response.status = 400
        return response.get_json_response()

    # Get the task_view model from the form
    form_task = input_form.save(commit=False)

    # TODO : try to put this check in the form validation
    # Get the task_view from the database
    try:
        task = Task.objects.get(id=task_id)
    except ObjectDoesNotExist:
        local_error = "La tache que vous voulez modifier n'existe pas."
        response.data.update({
            'success': False,
            'id': task_id,
            'local_error': local_error
        })
        response.status = 404
        return response.get_json_response()

    # If the task_view hash of the request doesn't correspond to the task_view hash of the database, throw an error
    database_task_hash = str(java_string_hashcode(task.text))
    if request_task_hash != database_task_hash:
        local_error = "Cette page a été modifié depuis la tentative de mise à jour."
        response.data.update({
            'success': False,
            'id': task_id,
            'local_error': local_error
        })
        response.status = 400
        return response.get_json_response()

    # Check if the user has the permission
    if not is_authorized_to_update_task(request.user, task):
        local_error = "L'utilisateur n'est pas authorisé à modifier cette tache"
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 403
        return response.get_json_response()

    # If all the above test are ok, update the task_view
    task.text = form_task.text
    task.is_achieved = form_task.is_achieved
    task.save()

    # Prepare the output data
    response.data.update({
        'success': True,
        'id': task.id
    })
    return response.get_json_response()


def delete_task(request):
    """
    Delete the given note_view.
    """
    # Initialize the output data
    response = JsonResponseContainer()

    # Get the task_view id from the request
    try:
        task_id = request.DELETE.get("id")
    except ObjectDoesNotExist:
        local_error = "La tache que vous voulez supprimer n'existe pas."
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 404
        return response.get_json_response()

    # Check if the user has the permission
    if not is_authorized_to_delete_task(request.user, task_id):
        local_error = "L'utilisateur n'est pas authorisé à supprimer cette tache"
        response.data.update({
            'success': False,
            'local_error': local_error
        })
        response.status = 403
        return response.get_json_response()

    # Delete the task_view
    Task.objects.filter(id=task_id).delete()

    # Prepare the output data
    response.data.update({
        'success': True,
        'id': task_id
    })
    return response.get_json_response()


@login_required
def task_view(request, codex_slug):
    """
    Manage REST like actions on a task_view.
    """
    # Create the output data
    http_status = HttpStatus()
    response = None

    try:
        if not request.is_ajax():
            raise_suspicious_operation(http_status)

        if request.method == 'POST':
            response = post_task(request, codex_slug)
        elif request.method == 'PUT':
            response = put_task(request)
        elif request.method == 'DELETE':
            response = delete_task(request)
        else:
            raise_suspicious_operation(http_status)

        # Return the output data
        return response
    except Exception as ex:
        # Return the error as a html page or as a JSON dictionary
        return render_error(request, ex, http_status)
