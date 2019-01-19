from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
import datetime

from django.urls import reverse

from projets.commun.codex import Page as Page_container
from projets.commun.error import HttpStatus, HttpNotFound
from projets.forms import TaskForm, NoteForm
from projets.models import Codex, Page, get_current_timestamp, Note, Task
from projets.views.codex_details_view import (
    get_today_page,
    get_pages_before_today,
    get_codex,
)


class GetTodayPageTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.client.login(username="zamour", password="top_secret")
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.empty_codex = Codex.objects.create(
            title="Test Codex 2", author=self.user, description="Description 2"
        )
        self.today = get_current_timestamp().date()
        self.page = Page.objects.create(codex=self.codex)
        Note.objects.create(page=self.page, text="Note test text")
        Task.objects.create(page=self.page, text="Task test text 1")
        Task.objects.create(page=self.page, text="Task test text 2")
        self.url = reverse("codex_details", kwargs={"codex_slug": self.codex.slug})

    def test_get_today_page_assert_return_page_container(self):
        page_container = get_today_page(self.empty_codex, self.today)

        self.assertIsInstance(page_container, Page_container)

    def test_get_today_page_not_exist_assert_return_page(self):
        page_container = get_today_page(self.empty_codex, self.today)

        self.assertEqual(page_container.date, self.today)
        self.assertIsNotNone(page_container.new_task_form)
        self.assertIsInstance(page_container.new_task_form, TaskForm)
        self.assertIsNotNone(page_container.note_form)
        self.assertIsInstance(page_container.note_form, NoteForm)
        self.assertEqual(len(page_container.tasks_form), 0)

    def test_get_today_page_exist_assert_return_page(self):
        page_container = get_today_page(self.codex, self.today)

        self.assertEqual(page_container.date, self.today)
        self.assertIsNotNone(page_container.new_task_form)
        self.assertIsInstance(page_container.new_task_form, TaskForm)
        self.assertIsNotNone(page_container.note_form)
        self.assertIsInstance(page_container.note_form, NoteForm)
        self.assertEqual(len(page_container.tasks_form), 2)
        self.assertIsInstance(page_container.tasks_form[0], TaskForm)

    def test_get_pages_before_today_new_codex_assert_empty_list(self):
        old_pages = get_pages_before_today(self.empty_codex, self.today)

        self.assertEqual(len(old_pages), 0)

    def test_get_pages_before_today_assert_list_not_empty(self):
        later = datetime.date(self.today.year + 1, self.today.month, self.today.day)
        old_pages = get_pages_before_today(self.codex, later)

        self.assertEqual(len(old_pages), 1)

    def test_get_pages_before_today_assert_list_of_type_page_container(self):
        later = datetime.date(self.today.year + 1, self.today.month, self.today.day)
        old_pages = get_pages_before_today(self.codex, later)

        self.assertIsInstance(old_pages[0], Page_container)

    def test_get_pages_before_today_assert_first_page_container_full(self):
        later = datetime.date(self.today.year + 1, self.today.month, self.today.day)
        old_pages = get_pages_before_today(self.codex, later)
        page_container = old_pages[0]

        self.assertEqual(page_container.date, self.today)
        self.assertIsNotNone(page_container.note_form)
        self.assertIsInstance(page_container.note_form, NoteForm)
        self.assertEqual(len(page_container.tasks_form), 2)
        self.assertIsInstance(page_container.tasks_form[0], TaskForm)

    def test_get_codex_assert_return_http_response(self):
        """ Test if the method return a HttpResponse """
        request = self.factory.get(self.url)
        response = get_codex(request, self.codex.slug)

        self.assertIsInstance(response, HttpResponse)

    def test_get_codex_view_assert_return_200(self):
        """ Test if the view return a 200 response to a get request"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_get_codex_codex_not_exist_assert_raise_not_found(self):
        """ Test if the method raise an error if the codex does not exist """
        slug = "TEST-KO"
        request = self.factory.get(reverse("information", kwargs={"codex_slug": slug}))
        with self.assertRaises(HttpNotFound):
            get_codex(request, slug)

    def test_delete_codex_view_assert_return_405(self):
        """ Test if the view return a 405 response to a delete request"""
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 405)

    def test_codex_details_view_not_connected_assert_return_connexion_page(self):
        """ Test if a un-connected user get the codex details """
        self.client.logout()

        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            "/connexion" + "?next=" + self.url,
            status_code=302,
            target_status_code=200,
        )
