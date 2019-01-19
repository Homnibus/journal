from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache

from ..commun.error import HttpMethodNotAllowed
from ..forms import CodexForm


def get_new_codex(request):
    """
    Return the page for the codex creation
    """
    # Create the output form
    output_form = CodexForm()
    # Prepare the output data
    output_data = {"form": output_form}
    return render(request, "projets/codex_add.html", output_data)


def post_new_codex(request):
    """
    Create the codex and redirect to the codex page
    """
    # Get the form
    input_form = CodexForm(request.POST)

    # If the form is not valid, throw an error
    if not input_form.is_valid():
        # Prepare the output data
        output_data = {"form": input_form}
        return render(request, "projets/codex_add.html", output_data, status=400)

    # Create the new Codex
    codex = input_form.save(author=request.user)

    # Redirect to the codex page
    return redirect("codex_details", codex_slug=codex.slug)


@login_required
@never_cache
def codex_add_view(request):
    """
    Manage the codex creation
    """
    if request.method == "GET" and not request.is_ajax():
        response = get_new_codex(request)
    elif request.method == "POST" and not request.is_ajax():
        response = post_new_codex(request)
    else:
        raise HttpMethodNotAllowed
    return response
