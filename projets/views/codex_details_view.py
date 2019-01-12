from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext
from django.views.decorators.cache import never_cache

from ..commun.codex import Page as Page_container
from ..commun.error import HttpStatus, render_error, raise_suspicious_operation
from ..forms import NoteForm, TaskForm
from ..models import get_current_timestamp, Page, Note, Task, Codex


def get_today_page(codex, today):
    """
    Return the page of the day
    """
    # Initialize output data
    output_page_data = Page_container(date=today)

    # Get the page of the day (use filter and first to have one object or None)
    today_page = Page.objects.filter(codex=codex, date=today).first()
    # If the page does not exist, create an empty one
    # Do not save it before the user create a note or a task
    if not today_page:
        today_page = Page(codex=codex, date=today)

    # Get the note of the day (use filter and first to have one object or None)
    today_note = Note.objects.filter(page=today_page).first()
    # If the note does not exist, create an empty one
    if not today_note:
        today_note = Note(page=today_page)

    # Add the note as a form to the page
    output_page_data.note_form = NoteForm(instance=today_note)

    # Add a new task form to the page
    output_page_data.new_task_form = TaskForm()

    # Get the tasks of the day
    today_tasks = list(Task.objects.filter(page=today_page).order_by("creation_date"))
    # Add each task as a form to the page
    for task in today_tasks:
        output_page_data.tasks_form.append(TaskForm(instance=task))

    return output_page_data


def get_pages_before_today(codex, today):
    """
    Return all the pages which were created before today for the given codex
    """
    # Initialize output data
    output_old_pages = []

    # Get all the pages which are older than today
    old_pages = list(Page.objects.filter(codex=codex, date__lt=today).order_by("date"))

    # For each page, get the note and the corresponding tasks
    for page in old_pages:
        page_container = Page_container(date=page.date)

        # Get the corresponding note
        note = Note.objects.filter(page=page).first()
        # Add the note as a form to the page container
        if note:
            page_container.note_form = NoteForm(instance=note)

        # Get the corresponding tasks
        tasks = list(Task.objects.filter(page=page).order_by("creation_date"))
        # Add each task as a form to the page container
        for task in tasks:
            page_container.tasks_form.append(TaskForm(instance=task))

        # Add the current page container to the output page list
        output_old_pages.append(page_container)

    return output_old_pages


def get_codex(request, codex_slug, http_status):
    """
    Return the page of the given codex
    """
    # Initialize the output data
    output_data = {}

    # Get the codex from the slug
    try:
        codex = Codex.objects.get(slug=codex_slug)
    except Codex.DoesNotExist:
        # TODO : factorise this
        http_status.status = 404
        http_status.message = gettext("The Codex does not exist.")
        http_status.explanation = gettext(
            "The Codex you are trying to access does not exist."
        )
        raise

    # Add the codex to the output data
    output_data.update({"codex": codex})

    # Get today date in the database to have only one provider of date
    today = get_current_timestamp().date()

    # Get the page of the day
    today_page = get_today_page(codex, today)

    # Add the page of the day to the output data
    output_data.update({"today_page": today_page})

    # Get the others older pages
    old_pages = get_pages_before_today(codex, today)

    # Add the older pages to the output data
    output_data.update({"older_pages": old_pages})

    return render(request, "projets/codex_details.html", output_data)


@login_required
@never_cache
def codex_details_view(request, codex_slug):
    """
    Manage the codex view
    """
    # Initialize the output
    response = None
    http_status = HttpStatus()

    try:
        if request.method == "GET":
            response = get_codex(request, codex_slug, http_status)
        else:
            raise_suspicious_operation(http_status)
        return response
    except Exception as ex:
        # Return the error as a html page or as a JSON dictionary
        return render_error(request, ex, http_status)
