from datetime import datetime, date

from django.contrib.auth.models import User
from django.test import TestCase

from projets.models import Codex, Page, Note, Task, Information


class CodexModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.title = "Test Codex 1"
        self.description = "Description 1"
        self.slug = "test-codex-1"
        self.codex = Codex.objects.create(
            title=self.title, author=self.user, description=self.description
        )

    def test_creation_assert_non_needed_param_exist(self):
        """ Test if the non required parameters are added after the creation of the model """
        self.assertIsNotNone(self.codex)
        self.assertEqual(self.codex.title, self.title)
        self.assertEqual(self.codex.slug, self.slug)
        self.assertEqual(self.codex.description, self.description)
        self.assertEqual(self.codex.author, self.user)
        self.assertIsInstance(self.codex.creation_date, datetime)
        self.assertIsInstance(self.codex.update_date, datetime)
        self.assertIsInstance(self.codex.nested_update_date, datetime)

    def test_creation_same_title_assert_slug_is_different(self):
        """ Test if the slug is not the same for to codex with the same title """
        codex = Codex.objects.create(
            title=self.title, author=self.user, description=self.description
        )

        self.assertIsNotNone(codex)
        self.assertNotEqual(codex.slug, self.slug)

    def test_assert_self_is_str(self):
        """ Test if str(self) is a string """
        self.assertIsInstance(str(self.codex), str)

    def test_get_absolute_url_assert_is_str(self):
        """ Test if the function return the url of the codex detail """
        self.assertIsInstance(self.codex.get_absolute_url(), str)


class PageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.page = Page.objects.create(codex=self.codex)

    def test_creation_assert_non_needed_param_exist(self):
        """ Test if the non required parameters are added after the creation of the model """
        self.assertIsNotNone(self.page)
        self.assertEqual(self.page.codex, self.codex)
        self.assertIsInstance(self.page.date, date)
        self.assertIsInstance(self.page.creation_date, datetime)
        self.assertIsInstance(self.page.nested_update_date, datetime)

    def test_creation_assert_codex_date_updated(self):
        """ Test if the codex date was updated """
        self.assertEqual(self.page.nested_update_date, self.codex.nested_update_date)

    def test_assert_self_is_str(self):
        """ Test if str(self) is a string """
        self.assertIsInstance(str(self.page), str)


class NoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.page = Page.objects.create(codex=self.codex)
        self.text = "Test Text"
        self.note = Note.objects.create(page=self.page, text=self.text)

    def test_creation_assert_non_needed_param_exist(self):
        """ Test if the non required parameters are added after the creation of the model """
        self.assertIsNotNone(self.note)
        self.assertEqual(self.note.page, self.page)
        self.assertIsInstance(self.note.creation_date, datetime)
        self.assertIsInstance(self.note.update_date, datetime)

    def test_creation_assert_codex_and_page_date_updated(self):
        """ Test if the codex and page date was updated """
        self.assertEqual(self.note.update_date, self.codex.nested_update_date)
        self.assertEqual(self.note.update_date, self.page.nested_update_date)

    def test_assert_self_is_str(self):
        """ Test if str(self) is a string """
        self.assertIsInstance(str(self.note), str)

    def test_get_absolute_url_assert_is_str(self):
        """ Test if the function return the url of the task detail """
        self.assertIsInstance(self.note.get_absolute_url(), str)

    def test_creation_with_no_page_assert_non_needed_param_exist(self):
        """ Test if the non required parameters are added after the creation of the model if the page does not exist"""
        self.note.delete()
        note = Note(text=self.text)
        note.save(codex=self.codex)

        self.assertIsNotNone(note)
        self.assertEqual(note.page, self.page)
        self.assertIsInstance(note.creation_date, datetime)
        self.assertIsInstance(note.update_date, datetime)


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.codex = Codex.objects.create(
            title="Test Codex", author=self.user, description="Description"
        )
        self.page = Page.objects.create(codex=self.codex)
        self.text = "Test Text"
        self.task = Task.objects.create(page=self.page, text=self.text)

    def test_creation_assert_non_needed_param_exist(self):
        """ Test if the non required parameters are added after the creation of the model """
        self.assertIsNotNone(self.task)
        self.assertEqual(self.task.page, self.page)
        self.assertEqual(self.task.text, self.text)
        self.assertIsInstance(self.task.creation_date, datetime)
        self.assertIsInstance(self.task.update_date, datetime)
        self.assertIsNone(self.task.achieved_date)
        self.assertEqual(self.task.is_achieved, False)

    def test_creation_assert_codex_and_page_date_updated(self):
        """ Test if the codex and page date was updated """
        self.assertEqual(self.task.update_date, self.codex.nested_update_date)
        self.assertEqual(self.task.update_date, self.page.nested_update_date)

    def test_assert_self_is_str(self):
        """ Test if str(self) is a string """
        self.assertIsInstance(str(self.task), str)

    def test_get_absolute_url_assert_is_str(self):
        """ Test if the function return the url of the task detail """
        self.assertIsInstance(self.task.get_absolute_url(), str)

    def test_achieved_assert_date_is_not_none(self):
        """ Test if the update date is updated """
        self.task.is_achieved = True
        self.task.save()

        self.assertIsInstance(self.task.achieved_date, datetime)
        self.assertEqual(self.task.is_achieved, True)

    def test_un_achieved_assert_date_is_none(self):
        """ Test if the update date is updated """
        self.task.is_achieved = True
        self.task.save()
        self.task.is_achieved = False
        self.task.save()

        self.assertIsNone(self.task.achieved_date)
        self.assertEqual(self.task.is_achieved, False)

    def test_creation_with_no_page_assert_non_needed_param_exist(self):
        """ Test if the non required parameters are added after the creation of the model if the page does not exist"""
        task = Task(text=self.text)
        task.save(codex=self.codex)

        self.assertIsNotNone(task)
        self.assertEqual(task.page, self.page)
        self.assertEqual(task.text, self.text)
        self.assertIsInstance(task.creation_date, datetime)
        self.assertIsInstance(task.update_date, datetime)
        self.assertIsNone(task.achieved_date)
        self.assertEqual(task.is_achieved, False)


class InformationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.text = " Test Text"
        self.information = Information.objects.create(codex=self.codex, text=self.text)

    def test_creation_assert_non_needed_param_exist(self):
        """ Test if the non required parameters are added after the creation of the model """
        self.assertIsNotNone(self.information)
        self.assertEqual(self.information.codex, self.codex)
        self.assertIsInstance(self.information.creation_date, datetime)
        self.assertIsInstance(self.information.update_date, datetime)

    def test_creation_assert_codex_date_updated(self):
        """ Test if the codex date was updated """
        self.assertEqual(self.information.update_date, self.codex.nested_update_date)

    def test_assert_self_is_str(self):
        """ Test if str(self) is a string """
        self.assertIsInstance(str(self.information), str)

    def test_get_absolute_url_assert_is_str(self):
        """ Test if the function return the url of the task detail """
        self.assertIsInstance(self.information.get_absolute_url(), str)
