from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.urls import reverse

from projets.commun.error import HttpStatus
from projets.commun.utils import java_string_hashcode
from projets.models import Codex, Page, Task
from projets.views import (
    is_authorized_to_create_task,
    is_authorized_to_update_task,
    is_authorized_to_delete_task,
    get_list_task,
    delete_task,
    put_task,
    post_task,
)


class TaskViewTest(TestCase):
    def setUp(self):
        self.text = "Test Text"
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.page = Page.objects.create(codex=self.codex)
        self.task = Task.objects.create(page=self.page, text=self.text)

    def test_is_authorized_to_create_task_user_is_author_task_assert_return_true(self):
        is_authorized = is_authorized_to_create_task(self.user, self.codex)

        self.assertEqual(is_authorized, True)

    def test_is_authorized_to_create_task_user_is_not_author_task_assert_return_false(
        self
    ):
        user = self.user = User.objects.create_user(
            username="test_user", email="test_user@test.com", password="admin"
        )
        is_authorized = is_authorized_to_create_task(user, self.codex)

        self.assertEqual(is_authorized, False)

    def test_is_authorized_to_update_task_user_is_author_task_assert_return_true(self):
        is_authorized = is_authorized_to_update_task(self.user, self.task)

        self.assertEqual(is_authorized, True)

    def test_is_authorized_to_update_task_user_is_not_author_task_assert_return_false(
        self
    ):
        user = self.user = User.objects.create_user(
            username="test_user", email="test_user@test.com", password="admin"
        )
        is_authorized = is_authorized_to_update_task(user, self.task)

        self.assertEqual(is_authorized, False)

    def test_is_authorized_to_delete_task_user_is_author_task_assert_return_true(self):
        is_authorized = is_authorized_to_delete_task(self.user, self.task.id)

        self.assertEqual(is_authorized, True)

    def test_is_authorized_to_delete_task_user_is_not_author_task_assert_return_false(
        self
    ):
        user = self.user = User.objects.create_user(
            username="test_user", email="test_user@test.com", password="admin"
        )
        is_authorized = is_authorized_to_delete_task(user, self.task.id)

        self.assertEqual(is_authorized, False)


class TaskListTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.client.login(username="zamour", password="top_secret")
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.http_status = HttpStatus()
        self.text = "Test Text"
        self.form_text = "Updated Test Text"
        self.form_is_achieved = True
        self.form_hash = str(java_string_hashcode(self.text))
        self.form_data = {
            "text": self.form_text,
            "is_achieved": self.form_is_achieved,
            "hash": self.form_hash,
        }
        self.page = Page.objects.create(codex=self.codex)
        self.task = Task.objects.create(page=self.page, text=self.text)
        self.url_list = reverse("tasks")
        self.url_list_filtered = reverse(
            "codex_tasks", kwargs={"codex_slug": self.codex.slug}
        )
        self.url_details = reverse("task_details", kwargs={"task_id": self.task.id})

    def test_get_list_task_assert_return_http_response(self):
        """ Test if the method return a HttpResponse """
        request = self.factory.get(self.url_list)
        request.user = self.user
        response = get_list_task(request)

        self.assertIsInstance(response, HttpResponse)

    def test_get_task_list_view_assert_return_200(self):
        """ Test if the view return a 200 response to a get request"""
        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, 200)

    def test_get_task_list_with_sort_by_view_assert_return_200(self):
        """ Test if the view return a 200 response to a get request"""
        form = {"sort_by": "is_achieved"}
        response = self.client.get(self.url_list, form)

        self.assertEqual(response.status_code, 200)

    def test_get_task_list_with_sort_by_and_sort_way_view_assert_return_200(self):
        """ Test if the view return a 200 response to a get request"""
        form = {"sort_by": "is_achieved", "sort_way": "desc"}
        response = self.client.get(self.url_list, form)

        self.assertEqual(response.status_code, 200)

    def test_get_task_list_with_negative_page_number_assert_return_200(self):
        """ Test if the view return a 200 response to a get request"""
        form = {"page_number": "-1"}
        response = self.client.get(self.url_list, form)

        self.assertEqual(response.status_code, 200)

    def test_get_task_list_filtered_view_assert_return_200(self):
        """ Test if the view return a 200 response to a get request"""
        response = self.client.get(self.url_list_filtered)

        self.assertEqual(response.status_code, 200)

    def test_delete_task_list_filtered_view_assert_return_405(self):
        """ Test if the view return a 200 response to a get request"""
        response = self.client.delete(self.url_list_filtered)

        self.assertEqual(response.status_code, 405)

    def test_task_list_view_not_connected_assert_return_connexion_page(self):
        """ Test if a un-connected user can list the tasks """
        self.client.logout()
        response = self.client.delete(self.url_list_filtered)

        self.assertRedirects(
            response,
            "/connexion" + "?next=" + self.url_list_filtered,
            status_code=302,
            target_status_code=200,
        )


class PostTaskTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.client.login(username="zamour", password="top_secret")
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.page = Page.objects.create(codex=self.codex)
        self.url_list = reverse("tasks")
        self.form_text = "Test Text"
        self.form_is_achieved = True
        self.form_data = {
            "text": self.form_text,
            "is_achieved": self.form_is_achieved,
            "codex_slug": self.codex.slug,
        }

    def test_post_task_assert_return_http_response(self):
        """ Test if the method return a HttpResponse """
        request = self.factory.post(self.url_list, self.form_data)
        request.user = self.user
        response = post_task(request)

        self.assertIsInstance(response, HttpResponse)

    def test_post_task_assert_task_created(self):
        """ Test if the method create the given task """
        request = self.factory.post(self.url_list, self.form_data)
        request.user = self.user
        post_task(request)
        task = Task.objects.get(text=self.form_text)

        self.assertEqual(task.text, self.form_text)
        self.assertEqual(task.is_achieved, self.form_is_achieved)

    def test_post_task_assert_other_task_not_updated(self):
        """ Test if the method does not update other task """
        text = "No update test text"
        Task.objects.create(page=self.page, text=text)
        request = self.factory.post(self.url_list, self.form_data)
        request.user = self.user
        post_task(request)
        tasks = Task.objects.all().order_by("id")

        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].text, text)
        self.assertEqual(tasks[0].is_achieved, False)

    def test_post_task_view_assert_return_200(self):
        """ Test if the view return a 200 response to a get request"""
        response = self.client.post(
            self.url_list, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 200)

    def test_post_task_view_text_empty_assert_return_400(self):
        """ Test if the view return a 200 response to a get request"""
        self.form_data["text"] = ""
        request = self.factory.post(self.url_list, self.form_data)
        request.user = self.user
        response = post_task(request)

        self.assertEqual(response.status_code, 400)

    def test_post_task_view_without_slug_assert_return_400(self):
        """ Test if the view return a 200 response to a get request"""
        del self.form_data["codex_slug"]
        request = self.factory.post(self.url_list, self.form_data)
        request.user = self.user
        response = post_task(request)

        self.assertEqual(response.status_code, 400)

    def test_post_task_view_codex_not_exist_assert_return_404(self):
        """ Test if the view return a 404 if the given slug does not exist """
        self.form_data["codex_slug"] = "slug-ko"
        request = self.factory.post(self.url_list, self.form_data)
        request.user = self.user
        response = post_task(request)

        self.assertEqual(response.status_code, 404)

    def test_post_task_of_other_user_assert_raise_403(self):
        """ Test if the method raise a 403 error the user has no right to update it """
        user = User.objects.create_user(
            username="tartine", email="tarnite@lelapin.com", password="top_secret"
        )
        request = self.factory.post(self.url_list, self.form_data)
        request.user = user
        response = post_task(request)

        self.assertEqual(response.status_code, 403)

    def test_delete_task_view_assert_return_405(self):
        """ Test if the view return a 405 response to a delete request"""
        response = self.client.delete(self.url_list)

        self.assertEqual(response.status_code, 405)

    def test_post_task_view_not_connected_assert_return_connexion_page(self):
        """ Test if a un-connected user can list the tasks """
        self.client.logout()
        response = self.client.delete(self.url_list)

        self.assertRedirects(
            response,
            "/connexion" + "?next=" + self.url_list,
            status_code=302,
            target_status_code=200,
        )


class PutTaskTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.client.login(username="zamour", password="top_secret")
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.text = "Test Text"
        self.form_text = "Updated Test Text"
        self.form_is_achieved = True
        self.form_hash = str(java_string_hashcode(self.text))
        self.form_data = {
            "text": self.form_text,
            "is_achieved": self.form_is_achieved,
            "hash": self.form_hash,
        }
        self.page = Page.objects.create(codex=self.codex)
        self.task = Task.objects.create(page=self.page, text=self.text)
        self.url_details = reverse("task_details", kwargs={"task_id": self.task.id})

    def test_put_task_assert_return_http_response(self):
        """ Test if the method return a HttpResponse """
        request = self.factory.post(self.url_details, self.form_data)
        request.user = self.user
        request.method = "PUT"
        request.PUT = request.POST
        response = put_task(request, self.task.id)

        self.assertIsInstance(response, HttpResponse)

    def test_put_task_assert_task_updated(self):
        """ Test if the method update the given task """
        request = self.factory.post(self.url_details, self.form_data)
        print(request.POST)
        request.user = self.user
        request.method = "PUT"
        request.PUT = request.POST
        put_task(request, self.task.id)

        task = Task.objects.get(id=self.task.id)

        self.assertEqual(task.text, self.form_text)
        self.assertEqual(task.is_achieved, self.form_is_achieved)

    def test_put_task_assert_other_task_not_updated(self):
        """ Test if the method does not update other task """
        text = "Test Text2"
        task = Task.objects.create(page=self.page, text=text)
        request = self.factory.post(self.url_details, self.form_data)
        request.user = self.user
        print(request.POST)
        request.method = "PUT"
        request.PUT = request.POST
        put_task(request, self.task.id)

        tasks = Task.objects.filter(id=task.id)

        self.assertEqual(tasks[0].text, text)
        self.assertEqual(tasks[0].is_achieved, False)

    def test_put_task_text_empty_assert_raise_400(self):
        """ Test if the method raise a 400 error if the form text is empty """
        self.form_data["text"] = ""
        request = self.factory.post(self.url_details, self.form_data)
        request.user = self.user
        request.method = "PUT"
        print(request.POST)
        request.PUT = request.POST
        response = put_task(request, self.task.id)

        self.assertEqual(response.status_code, 400)

    def test_put_task_does_not_exist_assert_raise_404(self):
        """ Test if the method raise a 404 error if the task does not exist """
        request = self.factory.post(self.url_details, self.form_data)
        print(request.POST)
        request.user = self.user
        request.method = "PUT"
        request.PUT = request.POST
        response = put_task(request, task_id=0)

        self.assertEqual(response.status_code, 404)

    def test_put_task_hash_invalid_assert_raise_400(self):
        """ Test if the method raise a 400 error if the text hash is not the same as the one of the database text """
        self.form_data["hash"] = "1"
        request = self.factory.post(self.url_details, self.form_data)
        print(request.POST)
        request.user = self.user
        request.method = "PUT"
        request.PUT = request.POST
        response = put_task(request, self.task.id)

        self.assertEqual(response.status_code, 400)

    def test_put_task_of_other_user_assert_raise_403(self):
        """ Test if the method raise a 403 error the user has no right to update it """
        user = User.objects.create_user(
            username="tartine", email="tarnite@lelapin.com", password="top_secret"
        )
        request = self.factory.post(self.url_details, self.form_data)
        print(request.POST)
        request.user = user
        request.method = "PUT"
        request.PUT = request.POST
        response = put_task(request, self.task.id)

        self.assertEqual(response.status_code, 403)

    def test_put_task_details_view_assert_input_invalid(self):
        """ Test if the view return a 400 response if there is not form data"""
        response = self.client.put(
            self.url_details, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 400)

    def test_post_task_details_view_assert_return_405(self):
        """ Test if the view return a 405 response to a get request"""
        response = self.client.post(
            self.url_details, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 405)


class DeleteTaskTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.client.login(username="zamour", password="top_secret")
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.text = "Test Text"
        self.form_text = "Updated Test Text"
        self.form_is_achieved = True
        self.form_hash = str(java_string_hashcode(self.text))
        self.form_data = {
            "text": self.form_text,
            "is_achieved": self.form_is_achieved,
            "hash": self.form_hash,
        }
        self.page = Page.objects.create(codex=self.codex)
        self.task = Task.objects.create(page=self.page, text=self.text)
        self.url_details = reverse("task_details", kwargs={"task_id": self.task.id})

    def test_delete_task_assert_return_http_response(self):
        """ Test if the method return a HttpResponse """
        request = self.factory.delete(self.url_details)
        request.user = self.user
        response = delete_task(request, self.task.id)

        self.assertIsInstance(response, HttpResponse)

    def test_delete_task_assert_delete_task(self):
        """ Test if the method return a HttpResponse """
        request = self.factory.delete(self.url_details)
        request.user = self.user
        task_id = self.task.id
        delete_task(request, task_id)
        tasks = Task.objects.filter(id=task_id)

        self.assertEqual(len(tasks), 0)

    def test_delete_task_assert_does_not_delete_other_task(self):
        """ Test if the method return a HttpResponse """
        task2 = Task.objects.create(page=self.page, text="Test Text2")
        request = self.factory.delete(self.url_details)
        request.user = self.user
        delete_task(request, self.task.id)
        tasks = Task.objects.filter(id=task2.id)

        self.assertEqual(len(tasks), 1)

    def test_delete_task_of_other_user_assert_return_error(self):
        """ Test if the method return a HttpResponse """
        user = User.objects.create_user(
            username="tartine", email="tarnite@lelapin.com", password="top_secret"
        )
        codex = Codex.objects.create(
            title="Test Codex 2", author=user, description="Description 2"
        )
        page = Page.objects.create(codex=codex)
        task = Task.objects.create(page=page, text="Test Text2")
        request = self.factory.delete(self.url_details)
        request.user = self.user
        delete_task(request, task.id)
        tasks = Task.objects.filter(id=task.id)

        self.assertEqual(len(tasks), 1)

    def test_delete_task_details_view_assert_return_200(self):
        """ Test if the view return a 200 response to a get request"""
        response = self.client.delete(
            self.url_details, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_task_details_view_not_ajax_assert_return_405(self):
        """ Test if the view return a 405 response to a get request"""
        response = self.client.delete(self.url_details)

        self.assertEqual(response.status_code, 405)

    def test_delete_task_view_not_connected_assert_return_connexion_page(self):
        """ Test if a un-connected user can list the tasks """
        self.client.logout()
        response = self.client.delete(self.url_details)

        self.assertRedirects(
            response,
            "/connexion" + "?next=" + self.url_details,
            status_code=302,
            target_status_code=200,
        )
