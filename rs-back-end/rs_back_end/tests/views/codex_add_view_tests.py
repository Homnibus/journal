from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.urls import reverse

from rs_back_end.models import Codex
from rs_back_end.views import get_new_codex, post_new_codex


class CodexAddViewTest(TestCase):
  def setUp(self):
    self.factory = RequestFactory()
    self.user = User.objects.create_user(
      username="zamour", email="zamour@zamour.com", password="top_secret"
    )
    self.client.login(username="zamour", password="top_secret")
    self.form_data = {"title": "Test Title", "description": "Test description"}
    self.slug = "test-title"

  def test_get_new_codex_assert_return_http_response(self):
    """ Test if the method return a HttpResponse """
    request = self.factory.get(reverse("codex_add"))
    response = get_new_codex(request)

    self.assertIsInstance(response, HttpResponse)

  def test_get_codex_add_view_assert_return_200(self):
    """ Test if the view return a 200 response to a get request"""
    response = self.client.get(reverse("codex_add"))

    self.assertEqual(response.status_code, 200)

  def test_post_new_codex_assert_return_http_response(self):
    """ Test if the method return a HttpResponse """
    request = self.factory.post(reverse("codex_add"))
    response = post_new_codex(request)

    self.assertIsInstance(response, HttpResponse)

  def test_post_new_codex_form_not_valid_assert_return_400(self):
    """ Test if the method return a 400 response if the form is not valid """
    request = self.factory.post(reverse("codex_add"))
    response = post_new_codex(request)

    self.assertEqual(response.status_code, 400)

  def test_post_new_codex_form_valid_assert_return_302(self):
    """ Test if the method return a 302 redirect response if the form is valid """
    request = self.factory.post(reverse("codex_add"), self.form_data)
    request.user = self.user

    response = post_new_codex(request)

    self.assertEqual(response.status_code, 302)

  def test_post_new_codex_form_valid_assert_create_codex(self):
    """ Test if the codex is created in the data base """
    request = self.factory.post(reverse("codex_add"), self.form_data)
    request.user = self.user
    post_new_codex(request)

    codex_list = Codex.objects.filter(title=self.form_data["title"])

    self.assertEqual(len(codex_list), 1)
    self.assertEqual(codex_list[0].title, self.form_data["title"])
    self.assertEqual(codex_list[0].slug, self.slug)
    self.assertEqual(codex_list[0].description, self.form_data["description"])

  def test_post_codex_add_view_assert_redirect_200(self):
    """ Test if the method return a 200 response after the redirect if the form is valid """
    response = self.client.post(reverse("codex_add"), self.form_data)
    codex_list = Codex.objects.filter(title=self.form_data["title"])

    self.assertRedirects(
      response,
      reverse("codex_details", kwargs={"codex_slug": codex_list[0].slug}),
      status_code=302,
      target_status_code=200,
    )

  def test_delete_codex_add_view_assert_return_405(self):
    """ Test if the method return a 405 response id the http method is not valid """
    response = self.client.delete(reverse("codex_add"))

    self.assertEqual(response.status_code, 405)

  def test_codex_add_view_not_connected_return(self):
    """ Test if a un-connected user can create a Codex """
    self.client.logout()

    response = self.client.post(reverse("codex_add"), self.form_data)
    codex_list = Codex.objects.filter(title=self.form_data["title"])

    self.assertEqual(len(codex_list), 0)
    self.assertRedirects(
      response,
      reverse("connexion") + "?next=" + reverse("codex_add"),
      status_code=302,
      target_status_code=200,
    )
