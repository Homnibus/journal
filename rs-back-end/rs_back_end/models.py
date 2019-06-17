from datetime import datetime

from django.contrib.auth.models import User
from django.db import models, connection
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext
from guardian.shortcuts import assign_perm


class Codex(models.Model):
  """
  A codex is like a diary book. It regroup information on a given subject.
  """

  title = models.CharField(
    "title", max_length=50, blank=False, null=False, help_text=gettext("Title of the codex")
  )
  slug = models.SlugField(
    "title slug",
    unique=True,
    max_length=50,
    blank=False,
    null=False,
    help_text=gettext("Slug created from the title"),
  )
  description = models.TextField(
    "description",
    blank=True,
    null=False,
    max_length=500,
    help_text=gettext("Description of the codex"),
  )
  author = models.ForeignKey(
    User,
    related_name="codex",
    editable=False,
    on_delete=models.SET_NULL,
    null=True,
    help_text=gettext("Creator of the codex"),
  )
  creation_date = models.DateTimeField(
    "creation date",
    editable=False,
    null=False,
    help_text=gettext("Date of creation of the codex"),
  )
  update_date = models.DateTimeField(
    "update date",
    editable=False,
    null=False,
    help_text=gettext("Date of last modification one of the codex information"),
  )
  nested_update_date = models.DateTimeField(
    "nested update date",
    editable=False,
    null=False,
    help_text=gettext("Date of last modification one of the codex element"),
  )

  class Meta:
    verbose_name = "codex"
    verbose_name_plural = "codex"

  def __str__(self):
    return self.title

  def save(self, *args, **kwargs):
    """
    Override the save method to generate the creation date and the title slug.
    """
    # At the creation of the codex
    if not self.id:
      # Set the creation date
      self.creation_date = get_current_timestamp()
      # Create a unique slug
      max_length = Codex._meta.get_field("slug").max_length
      self.slug = slugify(self.title)[:max_length]
      original_slug = self.slug
      # Add an id to the slug to get uniqueness
      i = 0
      while Codex.objects.filter(slug=self.slug).exists():
        i += 1
        # Truncate the original slug dynamically. Minus 1 for the hyphen.
        self.slug = "%s-%d" % (original_slug[: max_length - len(str(i)) - 1], i)
    # Set the codex update date
    self.update_date = get_current_timestamp()
    self.set_nested_update_date()
    # Save the codex
    super(Codex, self).save(*args, **kwargs)
    # Set user permissions
    if getattr(self, 'author', None) is not None:
      assign_all_perm(self, self.author)

  def get_absolute_url(self):
    return reverse("codex_details", kwargs={"codex_slug": self.slug})

  def set_nested_update_date(self):
    # Set the codex update date
    self.nested_update_date = get_current_timestamp()


class Page(models.Model):
  """
  A page regroup all the information of a given day in a codex.
  """

  # TODO: delete the page if there is no note and task on it anymore
  codex = models.ForeignKey(
    Codex,
    related_name="pages",
    unique_for_date="date",
    on_delete=models.CASCADE,
    null=False,
    editable=False,
    help_text=gettext("Codex of the page"),
  )
  date = models.DateField(
    "date", editable=False, null=False, help_text=gettext("Date of the page")
  )
  creation_date = models.DateTimeField(
    "creation date",
    editable=False,
    null=False,
    help_text=gettext("Date of creation of the page"),
  )
  nested_update_date = models.DateTimeField(
    "update date",
    editable=False,
    null=False,
    help_text=gettext("Date of last modification of an element of the page"),
  )

  class Meta:
    verbose_name = "page"
    verbose_name_plural = "pages"
    unique_together = ("codex", "date")

  def __str__(self):
    return gettext("Page for the {page_date}").format(page_date=self.creation_date)

  def save(self, *args, **kwargs):
    """
    Override the save method to generate the creation date.
    """
    # At the creation of the page
    if not self.id:
      # Set the page date
      self.date = get_current_timestamp().date()
      # Set the creation date
      self.creation_date = get_current_timestamp()
    # Set the page and codex nested_update_date
    self.set_nested_update_date()
    super(Page, self).save(*args, **kwargs)

  def set_nested_update_date(self):
    # Set the page update date
    self.nested_update_date = get_current_timestamp()
    # Set the codex update date
    self.codex.set_nested_update_date()
    self.codex.save()


class Note(models.Model):
  """
  A note record general information for a given page.
  """

  page = models.OneToOneField(
    Page,
    related_name="note",
    on_delete=models.CASCADE,
    null=False,
    editable=False,
    help_text=gettext("Note of the page"),
  )
  text = models.TextField("text", blank=False, null=False, help_text=gettext("Note text"))
  creation_date = models.DateTimeField(
    "creation date",
    editable=False,
    null=False,
    help_text=gettext("Date of creation of the note"),
  )
  update_date = models.DateTimeField(
    "update date",
    editable=False,
    null=False,
    help_text=gettext("Date of last modification of the note text"),
  )

  def __str__(self):
    return gettext("Note for the {note_date}").format(note_date=self.page.creation_date)

  def save(self, codex_id=None, *args, **kwargs):
    """
    Override the save method to generate the creation date.
    """
    # At the creation of the note
    if not self.id:
      # Set the creation date
      self.creation_date = get_current_timestamp()

    # Set the note update date
    self.update_date = get_current_timestamp()
    # Set the page nested_update_date
    self.page.set_nested_update_date()
    self.page.save()
    # Save the Note
    super(Note, self).save(*args, **kwargs)
    # Set user permissions
    if getattr(self.page.codex, 'author', None) is not None:
      assign_all_perm(self, self.page.codex.author)

  def get_absolute_url(self):
    return reverse("note_details", kwargs={"note_id": self.id})


class Task(models.Model):
  """
  A task record things to do for a given codex.
  """

  page = models.ForeignKey(
    Page,
    related_name="tasks",
    on_delete=models.CASCADE,
    null=False,
    editable=False,
    help_text="Tasks of the page",
  )
  text = models.TextField("text", blank=False, null=False, help_text=gettext("Task text"))
  is_achieved = models.BooleanField(
    "achieved", default=False, null=False, help_text=gettext("Task is achieved")
  )
  creation_date = models.DateTimeField(
    "creation date",
    editable=False,
    null=False,
    help_text=gettext("Date of creation of the task"),
  )
  update_date = models.DateTimeField(
    "update date",
    editable=False,
    null=False,
    help_text=gettext("Date of last modification of the task text or achievement status"),
  )
  achieved_date = models.DateTimeField(
    "achieved date",
    editable=False,
    null=True,
    help_text=gettext("Date of achievement of the task"),
  )

  def __init__(self, *args, **kwargs):
    super(Task, self).__init__(*args, **kwargs)
    self.initial_is_achieved = self.is_achieved

  def __str__(self):
    return gettext("Task {task_id} for the {task_date}").format(task_id=self.id, task_date=self.page.creation_date)

  def save(self, codex_id=None, *args, **kwargs):
    """
    Override the save method to generate the creation date and the is_achieved date.
    """
    # At the creation of the task
    if not self.id:
      # Set the creation date
      self.creation_date = get_current_timestamp()
      # Set the initial is_achieved to false to trigger the update of the achievement date
      self.initial_is_achieved = False

    # Set the achieved_date if the task has just been achieved
    if self.is_achieved is True and self.initial_is_achieved is False:
      self.achieved_date = get_current_timestamp()
      self.initial_is_achieved = True
    # Delete the achieved_date if the task has just been canceled
    if self.is_achieved is False and self.initial_is_achieved is True:
      self.achieved_date = None
      self.initial_is_achieved = False

    # Set the task update date
    self.update_date = get_current_timestamp()
    # Set the page nested_update_date
    self.page.set_nested_update_date()
    self.page.save()
    # Save the Task
    super(Task, self).save(*args, **kwargs)
    # Set user permissions
    if getattr(self.page.codex, 'author', None) is not None:
      assign_all_perm(self, self.page.codex.author)

  def get_absolute_url(self):
    return reverse("task_details", kwargs={"task_id": self.id})


class Information(models.Model):
  """
  General information of a given codex
  """

  codex = models.OneToOneField(
    Codex,
    related_name="information",
    on_delete=models.CASCADE,
    primary_key=False,
    null=False,
    editable=False,
    help_text=gettext("Codex of the information"),
  )
  text = models.TextField(
    "text", blank=False, null=False, help_text=gettext("Information text")
  )
  creation_date = models.DateTimeField(
    "creation date",
    editable=False,
    null=False,
    help_text=gettext("Date of creation of the information"),
  )
  update_date = models.DateTimeField(
    "update date",
    editable=False,
    null=False,
    help_text=gettext("Date of last modification of the information text"),
  )

  def __str__(self):
    return gettext("Information for the codex {codex_name}").format(codex_name=self.codex)

  def save(self, *args, **kwargs):
    """
    Override the save method to generate the creation date.
    """
    # At the creation of the information
    if not self.id:
      # Set the creation date
      self.creation_date = get_current_timestamp()
    # Set the information update date
    self.update_date = get_current_timestamp()
    # Set the codex nested_update_date
    self.codex.set_nested_update_date()
    self.codex.save()
    # Save the information
    super(Information, self).save(*args, **kwargs)
    # Set user permissions
    if getattr(self.codex, 'author', None) is not None:
      assign_all_perm(self, self.codex.author)

  def get_absolute_url(self):
    return reverse("information", kwargs={"codex_slug": self.codex.slug})


def assign_all_perm(model_instance, user):
  model_name = model_instance._meta.model_name
  assign_perm('view_{}'.format(model_name), user, model_instance)
  assign_perm('change_{}'.format(model_name), user, model_instance)
  assign_perm('delete_{}'.format(model_name), user, model_instance)


def get_current_timestamp():
  """
  Fonction qui récupère la base de la BDD pour n'avoir qu'une seul source de date qui n'est pas du tout optimisé !
  """
  cursor = connection.cursor()
  cursor.execute("select current_timestamp")
  sql_result = cursor.fetchone()
  if isinstance(sql_result[0], str):
    current_date = datetime.strptime(sql_result[0], "%Y-%m-%d %H:%M:%S")
  else:
    current_date = sql_result[0]

  return current_date
