from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.urls import reverse

from rs_back_end.commun.error import HttpForbidden, HttpInvalidFormData
from rs_back_end.commun.utils import java_string_hashcode
from rs_back_end.models import Codex, Page, Task
from rs_back_end.views import (
  is_authorized_to_create_task,
  is_authorized_to_update_task,
  is_authorized_to_delete_task,
  get_list_task,
  delete_task,
  put_task,
  post_task,
  is_authorized_to_get_task,
  JsonResponse,
)


class TaskPermissionTest(TestCase):
  def setUp(self):
    self.text = "Test Text"
    self.user = User.objects.create_user(
      username="zamour", email="zamour@zamour.com", password="top_secret"
    )
    self.other_user = User.objects.create_user(
      username="test_user", email="test_user@test.com", password="admin"
    )
    self.codex = Codex.objects.create(
      title="Test Codex 1", author=self.user, description="Description 1"
    )
    self.page = Page.objects.create(codex=self.codex)
    self.task = Task.objects.create(page=self.page, text=self.text)

  def test_is_authorized_to_get_task_user_is_author_assert_return_true(self):
    is_authorized = is_authorized_to_get_task(self.user, self.codex)
    self.assertEqual(is_authorized, True)

  def test_is_authorized_to_get_task_user_is_not_author_assert_return_false(self):
    is_authorized = is_authorized_to_get_task(self.other_user, self.codex)
    self.assertEqual(is_authorized, False)

  def test_is_authorized_to_create_task_user_is_author_assert_return_true(self):
    is_authorized = is_authorized_to_create_task(self.user, self.codex)
    self.assertEqual(is_authorized, True)

  def test_is_authorized_to_create_task_user_is_not_author_assert_return_false(self):
    is_authorized = is_authorized_to_create_task(self.other_user, self.codex)
    self.assertEqual(is_authorized, False)

  def test_is_authorized_to_update_task_user_is_author_assert_return_true(self):
    is_authorized = is_authorized_to_update_task(self.user, self.task)
    self.assertEqual(is_authorized, True)

  def test_is_authorized_to_update_task_user_is_not_author_assert_return_false(self):
    is_authorized = is_authorized_to_update_task(self.other_user, self.task)
    self.assertEqual(is_authorized, False)

  def test_is_authorized_to_delete_task_user_is_author_assert_return_true(self):
    is_authorized = is_authorized_to_delete_task(self.user, self.task)
    self.assertEqual(is_authorized, True)

  def test_is_authorized_to_delete_task_user_is_not_author_assert_return_false(self):
    is_authorized = is_authorized_to_delete_task(self.other_user, self.task)
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
    self.page = Page.objects.create(codex=self.codex)
    self.task = Task.objects.create(page=self.page, text="Test text")
    self.url_list = reverse("tasks_list")
    self.url_list_filtered = reverse(
      "tasks", kwargs={"codex_slug": self.codex.slug}
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


class TaskTodoListTest(TestCase):
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
    self.task = Task.objects.create(page=self.page, text="Test text")
    self.task = Task.objects.create(page=self.page, text="Test text2")
    self.task = Task.objects.create(page=self.page, text="Test text3", is_achieved=True)
    self.url_list = reverse("tasks_list")
    self.url_list_filtered = reverse(
      "tasks", kwargs={"codex_slug": self.codex.slug}
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
    self.url = reverse("tasks", kwargs={"codex_slug": self.codex.slug})
    self.form_text = "Test Text"
    self.form_is_achieved = True
    self.form_data = {"text": self.form_text, "is_achieved": self.form_is_achieved}
    self.request = self.factory.post(self.url, self.form_data)
    self.request.user = self.user

  def test_post_task_assert_return_http_response(self):
    """ Test if the method return a JsonResponse. """
    response = post_task(self.request, self.codex)

    self.assertIsInstance(response, JsonResponse)

  def test_post_task_form_valid_assert_task_created(self):
    """ Test if the model is created if the input data are valid. """
    post_task(self.request, self.codex)

    tasks = Task.objects.all()

    self.assertEqual(len(tasks), 1)
    self.assertEqual(tasks[0].text, self.form_text)
    self.assertEqual(tasks[0].is_achieved, self.form_is_achieved)

  def test_post_task_page_exist_form_valid_assert_task_created(self):
    """ Test if the model is created if the page of the day already exist. """
    page = Page.objects.create(codex=self.codex)
    post_task(self.request, self.codex)

    tasks = Task.objects.all()

    self.assertEqual(len(tasks), 1)
    self.assertEqual(tasks[0].text, self.form_text)
    self.assertEqual(tasks[0].is_achieved, self.form_is_achieved)
    self.assertEqual(tasks[0].page, page)

  def test_post_task_assert_other_task_not_updated(self):
    """ Test if the method does not update other task """
    page = Page.objects.create(codex=self.codex)
    text = "No update test text"
    Task.objects.create(page=page, text=text)
    post_task(self.request, self.codex)
    tasks = Task.objects.all().order_by("id")

    self.assertEqual(len(tasks), 2)
    self.assertEqual(tasks[0].text, text)
    self.assertEqual(tasks[0].is_achieved, False)

  def test_post_task_view_assert_return_200(self):
    """ Test if the method return a 200 response if the form is valid. """
    response = self.client.post(
      self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
    )

    self.assertEqual(response.status_code, 200)

  def test_post_task_view_text_empty_assert_return_invalid_form_data(self):
    """ Test if the view return a HttpInvalidFormData if the text is empty. """
    self.form_data["text"] = ""
    self.request = self.factory.post(self.url, self.form_data)
    self.request.user = self.user
    with self.assertRaises(HttpInvalidFormData):
      post_task(self.request, self.codex)

  def test_post_task_view_codex_not_exist_assert_raise_invalid_form_data(self):
    """ Test if the view return HttpInvalidFormData if the given slug does not exist """
    self.url = reverse("notes", kwargs={"codex_slug": "SLUG-NOT-EXISTS"})
    response = self.client.post(
      self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
    )
    self.assertEqual(response.status_code, 404)
    self.assertIsInstance(response, HttpResponse)

  def test_post_task_of_other_user_assert_raise_forbidden(self):
    """ Test if the method raise a HttpForbidden error the user has no right to update it """
    user = User.objects.create_user(
      username="tartine", email="tarnite@lelapin.com", password="top_secret"
    )
    self.request.user = user
    with self.assertRaises(HttpForbidden):
      post_task(self.request, self.codex)

  def test_delete_note_assert_return_405(self):
    """ Test if the view return a 405 response to a not ajax request. """
    response = self.client.delete(
      self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
    )
    self.assertEqual(response.status_code, 405)

  def test_post_task_assert_return_405(self):
    """ Test if the view return a 405 response to a delete request"""
    response = self.client.delete(self.url, self.form_data)

    self.assertEqual(response.status_code, 405)

  def test_post_task_view_not_connected_assert_return_connexion_page(self):
    """ Test if a un-connected user is redirected to the connexion page. """
    self.client.logout()
    response = self.client.post(
      self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
    )

    self.assertRedirects(
      response,
      "/connexion" + "?next=" + self.url,
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
    self.page = Page.objects.create(codex=self.codex)
    self.text = "Test Text"
    self.task = Task.objects.create(page=self.page, text=self.text)
    self.url = reverse("task_details", kwargs={"task_id": self.task.id})
    self.form_text = "Updated Test Text"
    self.form_is_achieved = True
    self.form_hash = str(java_string_hashcode(self.text))
    self.form_data = {
      "text": self.form_text,
      "is_achieved": self.form_is_achieved,
      "hash": self.form_hash,
    }
    self.request = self.factory.post(self.url, self.form_data)
    print(self.request.POST)
    self.request.user = self.user
    self.request.method = "PUT"
    self.request.PUT = self.request.POST

  def test_put_task_assert_return_http_response(self):
    """ Test if the method return a JsonResponse. """
    response = put_task(self.request, self.task)

    self.assertIsInstance(response, JsonResponse)

  def test_put_task_assert_task_updated(self):
    """ Test if the model is updated if the input data are valid. """
    put_task(self.request, self.task)

    task = Task.objects.get(id=self.task.id)

    self.assertEqual(task.text, self.form_text)
    self.assertEqual(task.is_achieved, self.form_is_achieved)

  def test_put_task_assert_other_task_not_updated(self):
    """ Test if the method does not update other model. """
    text = "Test Text2"
    Task.objects.create(page=self.page, text=text)
    put_task(self.request, self.task)

    tasks = Task.objects.all().order_by("id")

    self.assertEqual(len(tasks), 2)
    self.assertEqual(tasks[1].text, text)
    self.assertEqual(tasks[1].is_achieved, False)

  def test_put_task_form_valid_assert_return_200(self):
    """ Test if the method return a 200 response if the form is valid. """
    response = self.client.put(
      self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
    )

    self.assertEqual(response.status_code, 200)

  def test_put_task_text_empty_assert_raise_invalid_form_data(self):
    """ Test if the method raise a HttpInvalidFormData error if the form text is empty """
    self.form_data["text"] = ""
    self.request = self.factory.post(self.url, self.form_data)
    print(self.request.POST)
    self.request.user = self.user
    self.request.method = "PUT"
    self.request.PUT = self.request.POST
    with self.assertRaises(HttpInvalidFormData):
      put_task(self.request, self.task)

  def test_put_task_hash_invalid_assert_raise_invalid_form_data(self):
    """
    Test if the method raise a HttpInvalidFormData error if the text hash is not the same as the one of the
    database text.
    """
    self.form_data["hash"] = "1"
    self.request = self.factory.post(self.url, self.form_data)
    print(self.request.POST)
    self.request.user = self.user
    self.request.method = "PUT"
    self.request.PUT = self.request.POST
    with self.assertRaises(HttpInvalidFormData):
      put_task(self.request, self.task)

  def test_put_task_not_exist_assert_return_http_not_found(self):
    """ Test if the view return a 404 error if the given information does not exist. """
    self.task.delete()
    response = self.client.put(
      self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
    )
    self.assertEqual(response.status_code, 404)
    self.assertIsInstance(response, JsonResponse)

  def test_put_task_of_other_user_assert_raise_forbidden(self):
    """ Test if the method raise a HttpForbidden error the user has no right to update it """
    self.user = User.objects.create_user(
      username="tartine", email="tarnite@lelapin.com", password="top_secret"
    )
    self.request.user = self.user
    with self.assertRaises(HttpForbidden):
      put_task(self.request, self.task)

  def test_put_task_without_form_assert_input_invalid(self):
    """ Test if the view return a 400 response if there is not form data"""
    response = self.client.put(self.url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

    self.assertEqual(response.status_code, 400)

  def test_post_task_assert_return_405(self):
    """ Test if the view return a 405 response to a post request"""
    response = self.client.post(
      self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
    )

    self.assertEqual(response.status_code, 405)

  def test_put_task_not_ajax_assert_return_405(self):
    """ Test if the view return a 405 response to a not ajax request. """
    response = self.client.put(self.url, self.form_data)

    self.assertEqual(response.status_code, 405)

  def test_put_user_not_connected_assert_return_401(self):
    """ Test if a un-connected user is prompted to reconnect. """
    self.client.logout()
    response = self.client.put(
      self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
    )

    self.assertEqual(response.status_code, 401)


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
    self.page = Page.objects.create(codex=self.codex)
    self.task = Task.objects.create(page=self.page, text=self.text)
    self.form_hash = str(java_string_hashcode(self.text))
    self.form_data = {"hash": self.form_hash}
    self.url = reverse("task_details", kwargs={"task_id": self.task.id})
    self.request = self.factory.post(self.url, self.form_data)
    print(self.request.POST)
    self.request.user = self.user
    self.request.method = "DELETE"
    self.request.DELETE = self.request.POST

  def test_delete_task_assert_return_http_response(self):
    """ Test if the method return a JsonResponse """
    response = delete_task(self.request, self.task)

    self.assertIsInstance(response, JsonResponse)

  def test_delete_task_assert_task_deleted(self):
    """ Test if the model is deleted if the input data are valid. """
    delete_task(self.request, self.task)

    tasks = Task.objects.all()

    self.assertEqual(len(tasks), 0)

  def test_delete_task_assert_does_not_delete_other_task(self):
    """ Test if the method return a HttpResponse """
    text = "Test Text2"
    Task.objects.create(page=self.page, text=text)
    delete_task(self.request, self.task)
    tasks = Task.objects.all()

    self.assertEqual(len(tasks), 1)
    self.assertEqual(tasks[0].text, text)

  def test_delete_task_hash_invalid_assert_raise_invalid_form_data(self):
    """
    Test if the method raise a HttpInvalidFormData error if the text hash is not the same as the one of the
    database text.
    """
    self.form_data["hash"] = "1"
    self.request = self.factory.post(self.url, self.form_data)
    print(self.request.POST)
    self.request.user = self.user
    self.request.method = "PUT"
    self.request.DELETE = self.request.POST
    with self.assertRaises(HttpInvalidFormData):
      delete_task(self.request, self.task)

  def test_delete_task_of_other_user_assert_raise_forbidden(self):
    """ Try to delete the ask of an other user and assert the method raise an HttpForbidden error"""
    user = User.objects.create_user(
      username="tartine", email="tarnite@lelapin.com", password="top_secret"
    )
    codex = Codex.objects.create(
      title="Test Codex 2", author=user, description="Description 2"
    )
    page = Page.objects.create(codex=codex)
    task = Task.objects.create(page=page, text="Test Text2")
    self.request = self.factory.delete(self.url)
    self.request.user = self.user
    with self.assertRaises(HttpForbidden):
      delete_task(self.request, task)

  def test_delete_task_assert_return_200(self):
    """ Test if the view return a 200 response if the form is valid. """
    response = self.client.delete(self.url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

    self.assertEqual(response.status_code, 200)

  def test_post_task_assert_return_405(self):
    """ Test if the view return a 405 response to a put request. """
    response = self.client.post(self.url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

    self.assertEqual(response.status_code, 405)

  def test_delete_task_details_view_not_ajax_assert_return_405(self):
    """ Test if the view return a 405 response to a delete request. """
    response = self.client.delete(self.url)

    self.assertEqual(response.status_code, 405)

  def test_delete_task_view_not_connected_assert_return_401(self):
    """ Test if a un-connected user is prompted to reconnect. """
    self.client.logout()
    response = self.client.delete(self.url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

    self.assertEqual(response.status_code, 401)
