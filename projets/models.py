from datetime import datetime

from django.contrib.auth.models import User
from django.db import models, connection
from django.template.defaultfilters import slugify
from django.urls import reverse


class Codex(models.Model):
    """
    A codex is like a diary book. It regroup information on a given subject.
    """

    title = models.CharField(
        "title", max_length=50, blank=False, null=False, help_text="Title of the codex"
    )
    slug = models.SlugField(
        "title slug",
        unique=True,
        max_length=50,
        blank=False,
        null=False,
        help_text="Slug created from the title",
    )
    description = models.TextField(
        "description",
        blank=True,
        null=False,
        max_length=500,
        help_text="Description of the codex",
    )
    author = models.ForeignKey(
        User,
        related_name="codex",
        editable=False,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Creator of the codex",
    )
    creation_date = models.DateTimeField(
        "creation date",
        editable=False,
        null=False,
        help_text="Date of creation of the codex",
    )
    update_date = models.DateTimeField(
        "update date",
        editable=False,
        null=False,
        help_text="Date of last modification one of the codex information",
    )
    nested_update_date = models.DateTimeField(
        "nested update date",
        editable=False,
        null=False,
        help_text="Date of last modification one of the codex element",
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
        super(Codex, self).save(*args, **kwargs)

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
        help_text="Codex of the page",
    )
    date = models.DateField(
        "date", editable=False, null=False, help_text="Date of the page"
    )
    creation_date = models.DateTimeField(
        "creation date",
        editable=False,
        null=False,
        help_text="Date of creation of the page",
    )
    nested_update_date = models.DateTimeField(
        "update date",
        editable=False,
        null=False,
        help_text="Date of last modification of an element of the page",
    )

    class Meta:
        verbose_name = "page"
        verbose_name_plural = "pages"
        unique_together = ("codex", "date")

    def __str__(self):
        return "Page for the " + str(self.creation_date)

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


class Note(models.Model):
    """
    A note record general information for a given page.
    """

    page = models.OneToOneField(
        Page,
        related_name="note",
        on_delete=models.CASCADE,
        null=False,
        help_text="Note of the page",
    )
    text = models.TextField("text", blank=False, null=False, help_text="Note text")
    creation_date = models.DateTimeField(
        "creation date",
        editable=False,
        null=False,
        help_text="Date of creation of the note",
    )
    update_date = models.DateTimeField(
        "update date",
        editable=False,
        null=False,
        help_text="Date of last modification of the note text",
    )

    def __str__(self):
        return "Note for the " + str(self.page.creation_date)

    def save(self, commit=True, *args, **kwargs):
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
        super(Note, self).save(*args, **kwargs)

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
        help_text="Tasks of the page",
    )
    text = models.TextField("text", blank=False, null=False, help_text="Task text")
    is_achieved = models.BooleanField(
        "achieved", default=False, null=False, help_text="Task is achieved"
    )
    creation_date = models.DateTimeField(
        "creation date",
        editable=False,
        null=False,
        help_text="Date of creation of the task",
    )
    update_date = models.DateTimeField(
        "update date",
        editable=False,
        null=False,
        help_text="Date of last modification of the task text or achievement status",
    )
    achieved_date = models.DateTimeField(
        "achieved date",
        editable=False,
        null=True,
        help_text="Date of achievement of the task",
    )

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        self.initial_is_achieved = self.is_achieved

    def __str__(self):
        return "Task " + str(self.id) + " for the " + str(self.page.creation_date)

    def save(self, *args, **kwargs):
        """
        Override the save method to generate the creation date and the is_achieved date.
        """
        # At the creation of the task
        if not self.id:
            # Set the creation date
            self.creation_date = get_current_timestamp()

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
        super(Task, self).save(*args, **kwargs)

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
        help_text="Codex of the information",
    )
    text = models.TextField(
        "text", blank=False, null=False, help_text="Information text"
    )
    creation_date = models.DateTimeField(
        "creation date",
        editable=False,
        null=False,
        help_text="Date of creation of the information",
    )
    update_date = models.DateTimeField(
        "update date",
        editable=False,
        null=False,
        help_text="Date of last modification of the information text",
    )

    def __str__(self):
        return "Information for the codex " + str(self.codex)

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
        super(Information, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("information", kwargs={"codex_slug": self.codex.slug})


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
