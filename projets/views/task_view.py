from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.utils.translation import gettext

from projets.commun.error import HttpStatus, render_error, raise_suspicious_operation
from projets.commun.utils import (
    java_string_hashcode,
    JsonResponseContainer,
    min_paginator_rang,
    max_paginator_rang,
)
from projets.forms import TaskForm
from projets.models import Codex, Task


def is_authorized_to_create_task(user, codex):
    """
    Indicate if the user is authorized to create the task_details_view
    """
    if user == codex.author:
        return True
    return False


def is_authorized_to_update_task(user, task):
    """
    Indicate if the user is authorized to update the task_details_view
    """
    if user == task.page.codex.author:
        return True
    return False


def is_authorized_to_delete_task(user, task_id):
    """
    Indicate if the user is authorized to delete the task_details_view
    """
    # Get the task_details_view from the database
    task = Task.objects.get(id=task_id)
    if user == task.page.codex.author:
        return True
    return False


def get_list_task(request, codex_slug=None):
    """
    Get the list of all task owned by the user and matching the filters
    :param request: The input HTTP request
    :param codex_slug: The input HTTP request
    :return: the output HTTP request
    """
    # Initialize the output data
    output_data = {}

    # Get the tasks that the user is authorized to get
    task_list = Task.objects.filter(page__codex__author=request.user).select_related(
        "page__codex"
    )

    # If the request is made on a specific codex
    if codex_slug:
        # TODO : check if the user can see the codex ?
        # TODO : throw an error if the codex does not exist
        # Get the corresponding codex
        codex = Codex.objects.get(slug=codex_slug)
        # Filter the initial QuerySet
        task_list = task_list.filter(page__codex=codex)
        # Add the slug to the output date to filter the table
        output_data.update({"codex": codex})

    # Get the sort parameters
    sort_by = request.GET.get("sort_by")
    sort_way = request.GET.get("sort_way")
    sort_arg = []
    if sort_by in [
        "is_achieved",
        "text",
        "page__codex__title",
        "achieved_date",
        "creation_date",
    ]:
        if sort_way == "desc":
            sort_arg.append("-" + sort_by)
        else:
            sort_arg.append(sort_by)
    sort_arg.extend(["page__codex", "-page__date"])

    # Sort the QuerySet
    task_list = task_list.order_by(*sort_arg)

    # Update the output data with the initial sort parameters
    output_data.update({"sort_by": sort_by, "sort_way": sort_way})

    # Create the paginator
    paginator = Paginator(task_list, 10)

    # Get the asked page number
    paginator_page_number = int(request.GET.get("page_number", 1))

    # Get the corresponding page
    try:
        paginator_page = paginator.page(paginator_page_number)
    # If the page does not exist, return the first one
    except EmptyPage:
        paginator_page = paginator.page(1)
        paginator_page_number = 1

    # Update the output data with the current page
    output_data.update({"task_list": paginator_page})

    step = 2
    min_rang = min_paginator_rang(paginator_page_number, paginator.num_pages, step)
    max_rang = max_paginator_rang(paginator_page_number, paginator.num_pages, step)
    # Create a paginator rang to ease the navigation
    paginator_range = range(min_rang, max_rang + 1)
    # If the first page is not in the paginator range, set has_first to true
    if paginator_range[0] != 1:
        output_data.update({"has_first": True})
    # If the last page is not in the paginator range, set has_last to true
    if paginator_range[-1] != paginator.num_pages:
        output_data.update({"has_last": True})
    # Update the output data with the paginator rang
    output_data.update({"paginator_range": paginator_range})

    return render(request, "projets/task_list.html", output_data)


def post_task(request):
    """
    Create a new task_details_view for the given codex.
    """
    # Initialize the output data
    response = JsonResponseContainer()

    # Get the form
    input_form = TaskForm(request.POST)

    # If the form is not valid, throw an error
    if not input_form.is_valid():
        # TODO: review the form validation
        form_errors = gettext("Form validation error.")
        response.data.update({"success": False, "form_errors": form_errors})
        response.status = 400
        return response.get_json_response()

    # Get the task_details_view model from the form
    form_task = input_form.save(commit=False)

    # TODO: put this test in the form validation
    # If the task_details_view text is empty, throw an error
    if not form_task.text or form_task.text.isspace():
        local_error = gettext("Can't create an empty Task.")
        response.data.update({"success": False, "local_error": local_error})
        response.status = 400
        return response.get_json_response()

    # Get the codex of the task from the slug
    codex_slug = request.POST.get("codex_slug")

    # If the codex_slug is empty, throw an error
    if not codex_slug:
        form_errors = gettext("Form validation error.")
        response.data.update({"success": False, "form_errors": form_errors})
        response.status = 400
        return response.get_json_response()

    try:
        codex = Codex.objects.get(slug=codex_slug)
    except Codex.DoesNotExist:
        # TODO : factorise this
        local_error = gettext("The Codex does not exist.")
        response.data.update({"success": False, "local_error": local_error})
        response.status = 404
        return response.get_json_response()

    # Check if the user has the permission
    if not is_authorized_to_create_task(request.user, codex):
        local_error = gettext("You are not allowed to create this Task.")
        response.data.update({"success": False, "local_error": local_error})
        response.status = 403
        return response.get_json_response()

    # If all the above test are ok, create the task_details_view
    task = Task(text=form_task.text, is_achieved=form_task.is_achieved)
    task.save(codex=codex)

    # TODO : change the way this data is returned
    # Récupération du html d'un nouveau formulaire avec les données mises à jours pour affichage
    # et ajout aux données à retourner
    output_form = "<table>" + str(TaskForm(instance=task)) + "</table>"

    # Prepare the output data
    response.data.update({"success": True, "out_form": output_form, "id": task.id})
    return response.get_json_response()


def put_task(request, task_id):
    """
    Update the given task_details_view
    """
    # Initialize the output data
    response = JsonResponseContainer()

    # Get the form
    input_form = TaskForm(request.PUT)

    # TODO : get this information from the form
    # Get the task_details_view hash from the request
    request_task_hash = request.PUT.get("hash")

    # If the form is not valid, throw an error
    if not input_form.is_valid():
        # TODO : review the validation of the form
        # TODO : change the way error are returned to raise an error as in the other methods
        form_errors = gettext("Form validation error.")
        response.data.update(
            {"success": False, "id": task_id, "form_errors": form_errors}
        )
        response.status = 400
        return response.get_json_response()

    # Get the task_details_view model from the form
    form_task = input_form.save(commit=False)

    # TODO : try to put this check in the form validation
    # Get the task_details_view from the database
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        local_error = gettext("The Task you are trying to modify does not exist.")
        response.data.update(
            {"success": False, "id": task_id, "local_error": local_error}
        )
        response.status = 404
        return response.get_json_response()

    # If the task_details_view hash of the request doesn't correspond to the task_details_view hash of the database,
    # throw an error
    database_task_hash = str(java_string_hashcode(task.text))
    if request_task_hash != database_task_hash:
        local_error = gettext(
            "The Task has been modified since the last attempt of modification."
        )
        response.data.update(
            {"success": False, "id": task_id, "local_error": local_error}
        )
        response.status = 400
        return response.get_json_response()

    # Check if the user has the permission
    if not is_authorized_to_update_task(request.user, task):
        local_error = gettext("You are not allowed to modify this Task")
        response.data.update({"success": False, "local_error": local_error})
        response.status = 403
        return response.get_json_response()

    # If all the above test are ok, update the task_details_view
    task.text = form_task.text
    task.is_achieved = form_task.is_achieved
    task.save()

    # Prepare the output data
    response.data.update({"success": True, "id": task.id})
    return response.get_json_response()


def delete_task(request, task_id):
    """
    Delete the given note_details_view.
    """
    # Initialize the output data
    response = JsonResponseContainer()

    # Check if the user has the permission
    if not is_authorized_to_delete_task(request.user, task_id):
        # TODO : change the way error are returned to raise an error as in the other methods
        local_error = gettext("You are not allowed to delete this Task.")
        response.data.update({"success": False, "local_error": local_error})
        response.status = 403
        return response.get_json_response()

    # Delete the task_details_view
    Task.objects.filter(id=task_id).delete()

    # Prepare the output data
    response.data.update({"success": True, "id": task_id})
    return response.get_json_response()


@login_required
def task_details_view(request, task_id):
    """
    Manage REST like actions on a task_details_view.
    """
    # Create the output data
    http_status = HttpStatus()
    response = None

    try:
        if not request.is_ajax():
            raise_suspicious_operation(http_status)

        if request.method == "PUT":
            response = put_task(request, task_id)
        elif request.method == "DELETE":
            response = delete_task(request, task_id)
        else:
            raise_suspicious_operation(http_status)

        # Return the output data
        return response
    except Exception as ex:
        # Return the error as a html page or as a JSON dictionary
        return render_error(request, ex, http_status)


@login_required
def task_list_view(request):
    """
    Manage REST like actions: get list and post.
    """
    # Create the output data
    http_status = HttpStatus()
    response = None

    try:

        if request.method == "GET":
            response = get_list_task(request)
        elif request.method == "POST" and request.is_ajax():
            response = post_task(request)
        else:
            raise_suspicious_operation(http_status)

        # Return the output data
        return response
    except Exception as ex:
        # Return the error as a html page or as a JSON dictionary
        return render_error(request, ex, http_status)


@login_required
def task_list_filtered_view(request, codex_slug=None):
    """
    Manage REST like actions: get list filtered.
    """
    # Create the output data
    http_status = HttpStatus()
    response = None

    try:

        if request.method == "GET":
            response = get_list_task(request, codex_slug)
        else:
            raise_suspicious_operation(http_status)

        # Return the output data
        return response
    except Exception as ex:
        # Return the error as a html page or as a JSON dictionary
        return render_error(request, ex, http_status)
