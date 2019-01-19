from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projets.commun.error import HttpMethodNotAllowed
from projets.models import Codex


def get_codex(request):
    """
    Return codex of the current user
    """
    # Initialize output
    output_data = {}

    # Get all the codex
    codex_list = Codex.objects.filter(author=request.user).order_by(
        "-nested_update_date"
    )

    # Add the codex to the output data
    output_data.update({"codex_list": codex_list})

    return render(request, "projets/codex_list.html", output_data)


@login_required
def codex_list_view(request):
    """
    Manage the recent codex view
    """
    if request.method == "GET":
        response = get_codex(request)
    else:
        raise HttpMethodNotAllowed
    return response
