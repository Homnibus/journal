from datetime import datetime, time

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from ..commun.codex import Page
from ..commun.error import HttpStatus, render_error, raise_suspicious_operation
from ..forms import Journal_EntreeForm, TODO_EntreeForm
from ..models import Projet, Journal_Entree, TODO_Entree, get_current_timestamp


def get_today_page(codex, today):
    """
    Return the page of the day
    """
    # Initialize output data
    today_page = Page(date=today)
    
    # Get the note of the day
    today_note = Journal_Entree.objects.filter(
        projet=codex,
        date_creation__range=[
            datetime.combine(today, time.min),
            datetime.combine(today, time.max)
        ]
    ).first()
    # If there is no note created today, create a new one
    if today_note is None:
        today_note = Journal_Entree(projet=codex)
    
    # Add the note as a form to the page
    today_page.note_form = Journal_EntreeForm(instance=today_note)

    # Add a new task form to the page
    today_page.new_task_form = TODO_EntreeForm()

    # Get the tasks of the day
    today_tasks = list(TODO_Entree.objects.filter(
        projet=codex,
        date_creation__range=[
            datetime.combine(today, time.min),
            datetime.combine(today, time.max)
        ]
    ).order_by('date_creation'))

    # Add each task as a form to the page
    for task in today_tasks:
        today_page.tasks_form.append(TODO_EntreeForm(instance=task))

    return today_page

    
def get_pages_before_today(codex, today):
    """
    Return all the pages which were created before today for the given codex
    """
    # Initialize output data
    old_pages = []
    
    # Get all the notes which are older than today
    old_notes = list(Journal_Entree.objects.filter(
        projet=codex,
        date_creation__lt=datetime.combine(today, time.min)
    ).order_by('date_creation'))
    old_notes_counter = 0
    
    # Get all the tasks which are older than today
    old_tasks = TODO_Entree.objects.filter(
        projet=codex,
        date_creation__lt=datetime.combine(today, time.min)
    ).order_by('date_creation')
    old_tasks_counter = 0
    
    # Reconcile the note list with the task list according to their creation date
    while old_tasks_counter < len(old_tasks) or old_notes_counter < len(old_notes):
    
        # Find the min date between the current note and task
        if old_tasks_counter >= len(old_tasks):
            current_date = old_notes[old_notes_counter].date_creation.date()
        elif old_notes_counter >= len(old_notes):
            current_date = old_tasks[old_tasks_counter].date_creation.date()
        else:
            current_date = min(
                old_notes[old_notes_counter].date_creation,
                old_tasks[old_tasks_counter].date_creation
            ).date()
        
        # Initialize a page with the previous date
        current_page = Page(date=current_date)
        is_page_alone = True
        
        # Add the note to the current page
        while old_notes_counter < len(old_notes) and old_notes[old_notes_counter].date_creation.date() == current_date:
            # TODO :Add error if there is more than one note for the same day
            if not is_page_alone:
                print("ERROR")
            current_page.note_form = Journal_EntreeForm(instance=old_notes[old_notes_counter])
            old_notes_counter += 1
            is_page_alone = False
        
        # Add the tasks to then current page
        while old_tasks_counter < len(old_tasks) and old_tasks[old_tasks_counter].date_creation.date() == current_date:
            current_page.tasks_form.append(TODO_EntreeForm(instance=old_tasks[old_tasks_counter]))
            old_tasks_counter += 1
        
        # Add the current page to the output page list
        old_pages.append(current_page)

    return old_pages


def get_codex(request, codex_slug, http_status):
    """
    Return the page of the given codex
    """
    # Initialize the output data
    output_data = {}

    # Get the codex from the slug
    try:
        codex = Projet.objects.get(slug=codex_slug)
    except ObjectDoesNotExist:
        # TODO : factorise this
        http_status.status = 404
        http_status.message = "Le codex n'existe pas."
        http_status.explanation = "Le codex que vous voulez accéder n'existe pas."
        raise

    # Add the codex to the output data
    output_data.update({'codex': codex})

    # Get today date in the database to have only one provider of date
    today = get_current_timestamp()

    # Get the page of the day
    today_page = get_today_page(codex, today)

    # Add the page of the day to the output data
    output_data.update({'today_entry': today_page})

    # Get the others older pages
    old_pages = get_pages_before_today(codex, today)

    # Add the older pages to the output data
    output_data.update({'older_entry': old_pages})

    return render(request, 'projets/codex.html', output_data)


@login_required
@never_cache
def codex_view(request, codex_slug):
    """
    Manage the codex view
    """
    # Initialize the output
    response = None
    http_status = HttpStatus()

    try:
        if request.method == 'GET':
            response = get_codex(request, codex_slug, http_status)
        else:
            raise_suspicious_operation(http_status)
        return response
    except Exception as ex:
        # Return the error as a html page or as a JSON dictionary
        return render_error(request, ex, http_status)
