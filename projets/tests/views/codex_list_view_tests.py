from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.urls import reverse

from projets.commun.error import HttpStatus
from projets.models import Codex
from projets.views import get_codex


class CodexListViewTest(TestCase):
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
        self.form_data = {"text": self.text}
        self.url = reverse("codex")

    def test_get_codex_assert_return_http_response(self):
        """ Test if the method return a HttpResponse """
        request = self.factory.get(self.url)
        request.user = self.user
        response = get_codex(request)

        self.assertIsInstance(response, HttpResponse)

    def test_get_codex_view_assert_return_200(self):
        """ Test if the view return a 200 response to a get request"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_post_codex_view_assert_return_405(self):
        """ Test if the method return a 405 response if the http method is post """
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 405)

    def test_delete_codex_view_assert_return_405(self):
        """ Test if the method return a 405 response id the http method is not valid """
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 405)

    def test_codex_view_not_connected_assert_return_connexion_page(self):
        """ Test if a un-connected user can update the information """
        self.client.logout()
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            "/connexion" + "?next=" + self.url,
            status_code=302,
            target_status_code=200,
        )
