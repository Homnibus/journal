from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projets.commun.error import HttpStatus, raise_suspicious_operation, render_error
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
    # Initialize output
    http_status = HttpStatus()
    response = None

    try:
        if request.method == "GET":
            response = get_codex(request)
        else:
            raise_suspicious_operation(http_status)
        return response

    except Exception as ex:
        # Return the error as a html page or as a JSON dictionary
        return render_error(request, ex, http_status)
