from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from rs_back_end.models import Codex


def create_default_codex(user):
  author = user
  title = "text_editor"
  description = "Test codex for the new text editor"
  codex, created = Codex.objects.get_or_create(
    title=title, description=description, author=author
  )
  return codex


def get_text_editor(request):
  """
  Return the page of text editor demo
  """
  # Create the output date
  output_data = {}

  # Get the test Codex, create it if it does not exist
  codex = create_default_codex(request.user)

  # Add the Codex to the output data
  output_data.update({"codex": codex})

  return render(request, "rs_back_end/text_editor.html", output_data)


def post_text_editor(request):
  """
  Reset the Codex
  """
  # Create the output date
  output_data = {}

  # Delete the default codex
  author = request.user
  title = "text_editor"
  description = "Test codex for the new text editor"
  Codex.objects.get(title=title, description=description, author=author).delete()

  # Get the test Codex, create it if it does not exist
  codex = create_default_codex(request.user)

  # Add the Codex to the output data
  output_data.update({"codex": codex})

  return render(request, "rs_back_end/text_editor.html", output_data)


@login_required
@never_cache
def text_editor_view(request):
  """
  Manage text editor demo
  """
  # Initialize output
  response = None

  if request.method == "GET":
    response = get_text_editor(request)
  elif request.method == "POST":
    response = post_text_editor(request)
  return response
