from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from rs_back_end.commun.error import (
  HttpInvalidFormData,
  HttpForbidden,
  HttpMethodNotAllowed,
  HttpNotAuthorized,
)
from rs_back_end.commun.utils import (
  min_paginator_rang,
  max_paginator_rang,
  get_object_or_not_found,
  java_string_hashcode,
)
from rs_back_end.forms import TaskUpdateForm, TaskCreateForm, TaskDeleteForm
from rs_back_end.models import Codex, Task


def is_authorized_to_get_task(user, codex):
  """
  Return True if the user is authorized to get the task of the given codex.
  """
  if user == codex.author:
    return True
  return False


def is_authorized_to_create_task(user, codex):
  """
  Return True if the user is authorized to create the task.
  """
  if user == codex.author:
    return True
  return False


def is_authorized_to_update_task(user, task):
  """
  Return True if the user is authorized to update the task.
  """
  if user == task.page.codex.author:
    return True
  return False


def is_authorized_to_delete_task(user, task):
  """
  Return True if the user is authorized to delete the task.
  """
  # Get the task_details_view from the database
  if user == task.page.codex.author:
    return True
  return False


def get_list_task(request, codex=None):
  """
  Get the list of all task owned by the user and matching the filters
  """
  # Initialize the output data
  output_data = {}

  # Get the tasks that the user is authorized to get
  task_list = Task.objects.filter(page__codex__author=request.user).select_related(
    "page__codex"
  )

  # If the request is made on a specific codex
  if codex:
    # Check if the user has the permission to perform the action
    if not is_authorized_to_get_task(request.user, codex):
      raise HttpForbidden
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

  # TODO: Set this prop as a Const and put it in a conf file
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

  return render(request, "rs_back_end/task_list.html", output_data)


def get_task_todo_list(request, codex=None):
  """
  Get the list of all task owned by the user that are not achieved
  """
  # Initialize the output data
  output_data = {}

  # Get the un-achieved task
  task_list = Task.objects.filter(is_achieved=False).order_by("creation_date")

  # If the request is made on a specific codex
  if codex:
    # Check if the user has the permission to perform the action
    if not is_authorized_to_get_task(request.user, codex):
      raise HttpForbidden
    # Filter the initial QuerySet
    task_list = task_list.filter(page__codex=codex)
    # Add the slug to the output date to filter the table
    output_data.update({"codex": codex})

  task_form_list = []
  # Change the model list to a form list
  for task in task_list:
    task_form_list.append(TaskUpdateForm(instance=task))

  # Update the output data with the current page
  output_data.update({"task_list": task_form_list})

  return render(request, "rs_back_end/task_todo_list.html", output_data)


def post_task(request, codex):
  """
  Create a new task for the given codex and for the current day.
  """
  # Check if the user has the permission to perform the action
  if not is_authorized_to_create_task(request.user, codex):
    raise HttpForbidden

  # Initialise the django representation of a form with the input data
  input_form = TaskCreateForm(data=request.POST, codex=codex)

  # Check if the input data are valid
  if not input_form.is_valid():
    raise HttpInvalidFormData(
      form_errors=input_form.non_field_errors(),
      fields_error=input_form.errors.as_json(),
    )

  # Create the task
  task = input_form.save()

  # Get the created task hash to return it
  task_hash = java_string_hashcode(task.text)

  return JsonResponse({"success": True, "id": task.id, "hash": task_hash})


def put_task(request, task):
  """
  Update the given task.
  """
  # Check if the user has the permission to perform the action
  if not is_authorized_to_update_task(request.user, task):
    raise HttpForbidden

  # Initialise the django representation of a form with the input data
  input_form = TaskUpdateForm(request.PUT, instance=task)

  # Check if the input data are valid
  if not input_form.is_valid():
    raise HttpInvalidFormData(
      form_errors=input_form.non_field_errors(), fields_error=input_form.errors
    )

  # Update the task
  input_form.save()

  return JsonResponse({"success": True})


def delete_task(request, task):
  """
  Delete the given task.
  """
  # Check if the user has the permission to perform the action
  if not is_authorized_to_delete_task(request.user, task):
    raise HttpForbidden

  # Initialise the django representation of a form with the input data
  input_form = TaskDeleteForm(request.DELETE, instance=task)

  # Check if the input data are valid
  if not input_form.is_valid():
    raise HttpInvalidFormData(
      form_errors=input_form.non_field_errors(), fields_error=input_form.errors
    )

  # Delete the task
  task.delete()

  return JsonResponse({"success": True})


def task_details_view(request, task_id):
  """
  Manage the update and deletion of a task.
  """
  # Manually check if the user is connected to return a 401 error.
  if not request.user.is_authenticated:
    raise HttpNotAuthorized

  # Check if the requested resource exist
  task = get_object_or_not_found(Task, id=task_id)

  if request.method == "PUT" and request.is_ajax():
    response = put_task(request, task)
  elif request.method == "DELETE" and request.is_ajax():
    response = delete_task(request, task)
  else:
    raise HttpMethodNotAllowed

  return response


@never_cache
@login_required
def task_list_view(request, codex_slug):
  """
  Manage the listing and the creation of a task.
  """
  # Check if the requested resource exist
  codex = get_object_or_not_found(Codex, slug=codex_slug)

  if request.method == "GET" and not request.is_ajax():
    response = get_task_todo_list(request, codex)
  elif request.method == "POST" and request.is_ajax():
    response = post_task(request, codex)
  else:
    raise HttpMethodNotAllowed

  return response


@login_required
def task_list_filtered_view(request):
  """
  Manage the filtered listing of a task.
  """
  if request.method == "GET" and not request.is_ajax():
    response = get_list_task(request)
  else:
    raise HttpMethodNotAllowed

  return response
