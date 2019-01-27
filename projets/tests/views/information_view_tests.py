from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.test import TestCase, RequestFactory
from django.urls import reverse

from projets.commun.error import HttpInvalidFormData, HttpConflict, HttpForbidden
from projets.commun.utils import java_string_hashcode
from projets.models import Codex, Information
from projets.views import (
    get_information,
    post_information,
    is_authorized_to_create_information,
    is_authorized_to_update_information,
    is_authorized_to_get_information,
    put_information,
)


class InformationPermissionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.other_user = User.objects.create_user(
            username="test_user", email="test_user@test.com", password="admin"
        )

        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.information = Information.objects.create(
            text="Test Text", codex=self.codex
        )

    def test_is_authorized_to_create_user_is_author_assert_return_true(self):
        is_authorized = is_authorized_to_create_information(self.user, self.codex)

        self.assertEqual(is_authorized, True)

    def test_is_authorized_to_create_user_is_not_author_assert_return_false(self):
        is_authorized = is_authorized_to_create_information(self.other_user, self.codex)

        self.assertEqual(is_authorized, False)

    def test_is_authorized_to_update_user_is_author_assert_return_true(self):
        is_authorized = is_authorized_to_update_information(self.user, self.information)

        self.assertEqual(is_authorized, True)

    def test_is_authorized_to_update_user_is_not_author_assert_return_false(self):
        is_authorized = is_authorized_to_update_information(
            self.other_user, self.information
        )

        self.assertEqual(is_authorized, False)

    def test_is_authorized_to_get_user_is_author_assert_return_true(self):
        is_authorized = is_authorized_to_get_information(self.user, self.codex)

        self.assertEqual(is_authorized, True)

    def test_is_authorized_to_get_user_is_not_author_assert_return_false(self):
        is_authorized = is_authorized_to_get_information(self.other_user, self.codex)

        self.assertEqual(is_authorized, False)


class GetInformationTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.client.login(username="zamour", password="top_secret")
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.text = "Test text"
        self.information = Information.objects.create(codex=self.codex, text=self.text)
        self.url = reverse("informations", kwargs={"codex_slug": self.codex.slug})
        self.request = self.factory.get(self.url)
        self.request.user = self.user

    def test_get_information_assert_return_http_response(self):
        """ Test if the method return a HttpResponse. """
        response = get_information(self.request, self.codex)

        self.assertIsInstance(response, HttpResponse)

    def test_get_information_exist_assert_return_200(self):
        """ Test if the method return a 200 response if the information exist. """
        response = get_information(self.request, self.codex)

        self.assertEqual(response.status_code, 200)

    def test_get_information_not_exist_assert_return_200(self):
        """ Test if the method return a 200 response if the information does not exist. """
        self.information.delete()
        response = get_information(self.request, self.codex)

        self.assertEqual(response.status_code, 200)

    def test_get_information_codex_not_exist_assert_return_not_found(self):
        """ Test if the view return a 404 error if the given slug does not exist. """
        self.url = reverse("informations", kwargs={"codex_slug": "SLUG-NOT-EXISTS"})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response, HttpResponse)

    def test_get_information_other_user_assert_raise_forbidden(self):
        """ Test if the method raise a HttpForbidden error the user has no right to create it. """
        self.user = User.objects.create_user(
            username="tartine", email="tarnite@lelapin.com", password="top_secret"
        )
        self.request.user = self.user
        with self.assertRaises(HttpForbidden):
            get_information(self.request, self.codex)

    def test_put_http_method_assert_return_405(self):
        """ Test if the view return a 405 response to a delete request. """
        response = self.client.put(self.url)

        self.assertEqual(response.status_code, 405)

    def test_get_ajax_assert_return_405(self):
        """ Test if the view return a 405 response to a not ajax request. """
        response = self.client.get(self.url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.assertEqual(response.status_code, 405)

    def test_post_user_not_connected_assert_redirect_to_connexion_page(self):
        """ Test if a un-connected user is redirected to the connexion page. """
        self.client.logout()
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            "/connexion" + "?next=" + self.url,
            status_code=302,
            target_status_code=200,
        )


class PostInformationTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.client.login(username="zamour", password="top_secret")
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.url = reverse("informations", kwargs={"codex_slug": self.codex.slug})
        self.text = "Test Text"
        self.form_data = {"text": self.text}
        self.request = self.factory.post(self.url, self.form_data)
        self.request.user = self.user

    def test_post_information_assert_return_json_response(self):
        """ Test if the method return a JsonResponse. """
        response = post_information(self.request, self.codex)

        self.assertIsInstance(response, JsonResponse)

    def test_post_information_form_valid_assert_create_information(self):
        """ Test if the model is created if the input data are valid. """
        post_information(self.request, self.codex)

        informations = Information.objects.all()

        self.assertEqual(len(informations), 1)
        self.assertEqual(informations[0].text, self.text)
        self.assertEqual(informations[0].codex, self.codex)

    def test_post_information_already_exist_assert_raise_http_conflict(self):
        """ Test if method raise a HttpConflict error if the model already exist. """
        Information.objects.create(codex=self.codex, text=self.text)
        with (self.assertRaises(HttpConflict)):
            post_information(self.request, self.codex)

    def test_post_information_assert_other_information_not_updated(self):
        """ Test if the method does not update other model. """
        codex = Codex.objects.create(
            title="Test Codex 2", author=self.user, description="Description 2"
        )
        text = "No update test text"
        Information.objects.create(codex=codex, text=text)
        post_information(self.request, self.codex)

        informations = Information.objects.all().order_by("id")

        self.assertEqual(len(informations), 2)
        self.assertEqual(informations[0].text, text)
        self.assertEqual(informations[0].codex, codex)

    def test_post_information_form_valid_assert_return_200(self):
        """ Test if the method return a 200 response if the form is valid. """
        response = self.client.post(
            self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 200)

    def test_post_information_text_empty_assert_return_invalid_form_data(self):
        """ Test if the method return a HttpInvalidFormData response if the input text is empty. """
        self.form_data["text"] = ""
        self.request = self.factory.post(self.url, self.form_data)
        self.request.user = self.user
        with self.assertRaises(HttpInvalidFormData):
            post_information(self.request, self.codex)

    def test_post_information_codex_not_exist_assert_return_not_found(self):
        """ Test if the view return a 404 error if the given slug does not exist. """
        self.url = reverse("informations", kwargs={"codex_slug": "SLUG-NOT-EXISTS"})
        response = self.client.post(
            self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response, JsonResponse)

    def test_post_information_other_user_assert_raise_forbidden(self):
        """ Test if the method raise a HttpForbidden error the user has no right to create it. """
        self.user = User.objects.create_user(
            username="tartine", email="tarnite@lelapin.com", password="top_secret"
        )
        self.request.user = self.user
        with self.assertRaises(HttpForbidden):
            post_information(self.request, self.codex)

    def test_delete_http_method_assert_return_405(self):
        """ Test if the view return a 405 response to a delete request. """
        response = self.client.delete(
            self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 405)

    def test_post_not_ajax_assert_return_405(self):
        """ Test if the view return a 405 response to a non ajax request. """
        response = self.client.post(self.url, self.form_data)

        self.assertEqual(response.status_code, 405)

    def test_post_user_not_connected_assert_redirect_to_connexion_page(self):
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


class PutInformationTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.client.login(username="zamour", password="top_secret")
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.text = "Test text"
        self.information = Information.objects.create(codex=self.codex, text=self.text)
        self.url = reverse("information", kwargs={"codex_slug": self.codex.slug})

        self.form_text = "Updated test text"
        self.form_hash = str(java_string_hashcode(self.text))
        self.form_data = {"text": self.form_text, "hash": self.form_hash}
        self.request = self.factory.post(self.url, self.form_data)
        print(self.request.POST)
        self.request.user = self.user
        self.request.method = "PUT"
        self.request.PUT = self.request.POST

    def test_put_information_assert_return_json_response(self):
        """ Test if the method return a JsonResponse. """
        response = put_information(self.request, self.information)

        self.assertIsInstance(response, JsonResponse)

    def test_put_information_form_valid_assert_information_updated(self):
        """ Test if the model is updated if the input data are valid. """
        put_information(self.request, self.information)

        information = Information.objects.get(id=self.information.id)

        self.assertEqual(information.text, self.form_text)

    def test_put_information_assert_other_information_not_updated(self):
        """ Test if the method does not update other model. """
        codex = Codex.objects.create(
            title="Test Codex 2", author=self.user, description="Description 2"
        )
        text = "No update test text"
        Information.objects.create(codex=codex, text=text)
        put_information(self.request, self.information)

        informations = Information.objects.all().order_by("id")

        self.assertEqual(len(informations), 2)
        self.assertEqual(informations[1].text, text)
        self.assertEqual(informations[1].codex, codex)

    def test_put_information_form_valid_assert_return_200(self):
        """ Test if the method return a 200 response if the form is valid. """
        response = self.client.put(
            self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 200)

    def test_put_information_text_empty_assert_raise_invalid_form_data(self):
        """ Test if the method return a HttpInvalidFormData response if the input text is empty. """
        self.form_data["text"] = ""
        self.request = self.factory.post(self.url)
        print(self.request.POST)
        self.request.user = self.user
        self.request.method = "PUT"
        self.request.PUT = self.request.POST
        with self.assertRaises(HttpInvalidFormData):
            put_information(self.request, self.information)

    def test_put_information_hash_invalid_assert_raise_invalid_form_data(self):
        """
        Test if the method raise a HttpInvalidFormData error if the text hash is not the same as the one of the
        database text.
        """
        self.form_data["hash"] = "1"
        self.request = self.factory.post(self.url)
        print(self.request.POST)
        self.request.user = self.user
        self.request.method = "PUT"
        self.request.PUT = self.request.POST
        with self.assertRaises(HttpInvalidFormData):
            put_information(self.request, self.information)

    def test_put_information_not_exist_assert_return_http_not_found(self):
        """ Test if the view return a 404 error if the given information does not exist. """
        self.information.delete()
        response = self.client.put(
            self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response, JsonResponse)

    def test_put_information_codex_not_exist_assert_return_not_found(self):
        """ Test if the view return a 404 error if the given slug does not exist. """
        self.url = reverse("informations", kwargs={"codex_slug": "SLUG-NOT-EXISTS"})
        response = self.client.put(
            self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response, JsonResponse)

    def test_put_information_of_other_user_assert_raise_forbidden(self):
        """ Test if the method raise a HttpForbidden error the user has no right to create it. """
        self.user = User.objects.create_user(
            username="tartine", email="tarnite@lelapin.com", password="top_secret"
        )
        self.request.user = self.user
        with self.assertRaises(HttpForbidden):
            put_information(self.request, self.information)

    def test_put_information_without_form_assert_input_invalid(self):
        """ Test if the view return a 400 response if there is not input form. """
        response = self.client.put(self.url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.assertEqual(response.status_code, 400)

    def test_post_http_method_assert_return_405(self):
        """ Test if the view return a 405 response to a post request. """
        response = self.client.post(
            self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 405)

    def test_put_not_ajax_assert_return_405(self):
        """ Test if the view return a 405 response to a not ajax request. """
        response = self.client.put(self.url, self.form_data)

        self.assertEqual(response.status_code, 405)

    def test_put_user_not_connected_assert_redirect_to_connexion_page(self):
        """ Test if a un-connected user is redirected to the connexion page. """
        self.client.logout()
        response = self.client.put(
            self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertRedirects(
            response,
            "/connexion" + "?next=" + self.url,
            status_code=302,
            target_status_code=200,
        )
