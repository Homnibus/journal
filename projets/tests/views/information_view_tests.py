from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.test import TestCase, RequestFactory
from django.urls import reverse

from projets.commun.error import HttpStatus
from projets.models import Codex, Information
from projets.views import get_information, post_information


class InformationViewTest(TestCase):
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
        self.url = reverse("information", kwargs={"codex_slug": self.codex.slug})

    def test_get_information_assert_return_http_response(self):
        """ Test if the method return a HttpResponse """
        request = self.factory.get(self.url)
        response = get_information(request, self.codex.slug, self.http_status)

        self.assertIsInstance(response, HttpResponse)

    def test_get_information_view_assert_return_200(self):
        """ Test if the view return a 200 response to a get request"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_get_information_codex_not_exist_assert_raise_not_exist(self):
        """ Test if the method raise an error if the codex does not exist """
        slug = "TEST-KO"
        request = self.factory.get(reverse("information", kwargs={"codex_slug": slug}))
        with self.assertRaises(Codex.DoesNotExist):
            get_information(request, slug, self.http_status)

    def test_get_information_codex_not_exist_assert_http_status_not_empty(self):
        """ Test if the method update the http status if the codex does not exist """
        slug = "TEST-KO"
        request = self.factory.get(reverse("information", kwargs={"codex_slug": slug}))
        try:
            get_information(request, slug, self.http_status)
        except:
            pass

        self.assertNotEqual(self.http_status.status, 200)
        self.assertNotEqual(self.http_status.explanation, "")
        self.assertNotEqual(self.http_status.message, "")

    def test_post_information_assert_return_json_response(self):
        """ Test if the method return a HttpResponse """
        request = self.factory.post(self.url)
        response = post_information(request, self.codex.slug)

        self.assertIsInstance(response, JsonResponse)

    def test_post_information_form_not_valid_assert_return_400(self):
        """ Test if the method return a 400 response if the form is not valid """
        request = self.factory.post(self.url)
        response = post_information(request, self.codex.slug)

        self.assertEqual(response.status_code, 400)

    def test_post_information_form_valid_assert_return_200(self):
        """ Test if the method return a 200 response if the form is valid """
        response = self.client.post(
            self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 200)

    def test_post_information_form_valid_assert_create_information(self):
        """ Test if the codex is created in the data base """
        request = self.factory.post(self.url, self.form_data)
        post_information(request, self.codex.slug)

        informations = Information.objects.all()

        self.assertEqual(len(informations), 1)
        self.assertEqual(informations[0].text, self.text)
        self.assertEqual(informations[0].codex, self.codex)

    def test_post_information_form_valid_assert_update_information(self):
        """ Test if the codex is created in the data base """
        self.information = Information.objects.create(codex=self.codex, text=self.text)
        text = "Test Text 2"
        form_data = {"text": text}
        request = self.factory.post(self.url, form_data)
        post_information(request, self.codex.slug)

        informations = Information.objects.all()

        self.assertEqual(informations[0].text, text)

    def test_post_information_form_valid_assert_no_creation(self):
        """ Test if the codex is created in the data base """
        self.information = Information.objects.create(codex=self.codex, text=self.text)
        text = "Test Text 2"
        form_data = {"text": text}
        request = self.factory.post(self.url, form_data)
        post_information(request, self.codex.slug)

        informations = Information.objects.all()

        self.assertEqual(len(informations), 1)

    def test_post_information_codex_not_exist_assert_return_404(self):
        """ Test if the codex is created in the data base """
        request = self.factory.post(self.url, self.form_data)
        response = post_information(request, "TEST-SLUG-KO")

        self.assertEqual(response.status_code, 404)

    def test_delete_information_view_assert_return_405(self):
        """ Test if the method return a 405 response id the http method is not valid """
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 405)

    def test_information_view_not_connected_assert_return_connexion_page(self):
        """ Test if a un-connected user can update the information """
        self.client.logout()

        response = self.client.post(self.url, self.form_data)
        informations = Information.objects.all()

        self.assertEqual(len(informations), 0)
        self.assertRedirects(
            response,
            "/connexion" + "?next=" + self.url,
            status_code=302,
            target_status_code=200,
        )
