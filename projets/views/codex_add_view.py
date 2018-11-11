from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from ..forms import CodexForm
from ..commun.error import HttpStatus, render_error, raise_suspicious_operation


def get_new_codex(request):
    """
    Return the page for the codex creation
    """
    # Create the output form
    output_form = CodexForm()
    # Prepare the output data
    output_data = {'form': output_form}
    return render(request, 'projets/codex_add.html', output_data)


def post_new_codex(request):
    """
    Create the codex and redirect to the codex page
    """
    # Get the form
    input_form = CodexForm(request.POST)

    # If the form is not valid, throw an error
    if not input_form.is_valid():
        # Prepare the output data
        output_data = {'form': input_form}
        # TODO : manage form error
        return render(request, 'projets/codex_add.html', output_data)

    # Create the new Codex
    codex = input_form.save(commit=False)
    codex.author = request.user
    codex.save()

    # Redirect to the codex page
    return redirect('codex', codex_slug=codex.slug)


@login_required
@never_cache
def codex_add_view(request):
    """
    Manage the codex creation
    """
    # Initialize output
    http_status = HttpStatus()
    response = None

    try:
        if request.method == 'GET':
            response = get_new_codex(request)
        elif request.method == 'POST':
            response = post_new_codex(request)
        else:
            raise_suspicious_operation(http_status)
        return response

    except Exception as ex:
        # Return the error as a html page or as a JSON dictionary
        return render_error(request, ex, http_status)
