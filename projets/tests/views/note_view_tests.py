from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.test import TestCase, RequestFactory
from django.urls import reverse

from projets.commun.error import HttpForbidden, HttpInvalidFormData, HttpConflict
from projets.commun.utils import java_string_hashcode
from projets.models import Codex, Page, Note
from projets.views import (
    is_authorized_to_create_note,
    is_authorized_to_update_note,
    is_authorized_to_delete_note,
    post_note,
    delete_note,
    put_note,
)


class NotePermissionTest(TestCase):
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
        self.page = Page.objects.create(codex=self.codex)
        self.note = Note.objects.create(page=self.page, text="Test Text")

    def test_is_authorized_to_create_note_user_is_author_assert_return_true(self):
        is_authorized = is_authorized_to_create_note(self.user, self.codex)

        self.assertEqual(is_authorized, True)

    def test_is_authorized_to_create_note_user_is_not_author_assert_return_false(self):
        is_authorized = is_authorized_to_create_note(self.other_user, self.codex)

        self.assertEqual(is_authorized, False)

    def test_is_authorized_to_update_note_user_is_author_assert_return_true(self):
        is_authorized = is_authorized_to_update_note(self.user, self.note)

        self.assertEqual(is_authorized, True)

    def test_is_authorized_to_update_note_user_is_not_author_assert_return_false(self):
        is_authorized = is_authorized_to_update_note(self.other_user, self.note)

        self.assertEqual(is_authorized, False)

    def test_is_authorized_to_delete_note_user_is_author_assert_return_true(self):
        is_authorized = is_authorized_to_delete_note(self.user, self.note)

        self.assertEqual(is_authorized, True)

    def test_is_authorized_to_delete_note_user_is_not_author_assert_return_false(self):
        is_authorized = is_authorized_to_delete_note(self.other_user, self.note)

        self.assertEqual(is_authorized, False)


class PostNoteTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.client.login(username="zamour", password="top_secret")
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.url = reverse("notes", kwargs={"codex_slug": self.codex.slug})
        self.text = "Test Text"
        self.form_data = {"text": self.text}
        self.request = self.factory.post(self.url, self.form_data)
        self.request.user = self.user

    def test_post_note_assert_return_json_response(self):
        """ Test if the method return a JsonResponse. """
        response = post_note(self.request, self.codex)

        self.assertIsInstance(response, JsonResponse)

    def test_post_note_form_valid_assert_note_created(self):
        """ Test if the model is created if the input data are valid. """
        post_note(self.request, self.codex)

        notes = Note.objects.all()

        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].text, self.text)

    def test_post_information_already_exist_assert_raise_http_conflict(self):
        """ Test if method raise a HttpConflict error if the model already exist. """
        post_note(self.request, self.codex)

        with (self.assertRaises(HttpConflict)):
            post_note(self.request, self.codex)

    def test_post_note_page_exist_form_valid_assert_note_created(self):
        """ Test if the model is created if the page of the day already exist. """
        page = Page.objects.create(codex=self.codex)
        post_note(self.request, self.codex)

        notes = Note.objects.all()

        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].text, self.text)
        self.assertEqual(notes[0].page, page)

    def test_post_note_assert_other_note_not_updated(self):
        """ Test if the method does not update other model. """
        codex = Codex.objects.create(
            title="Test Codex 2", author=self.user, description="Description 2"
        )
        page = Page.objects.create(codex=codex)
        text = "No update test text"
        Note.objects.create(page=page, text=text)
        post_note(self.request, self.codex)

        notes = Note.objects.all().order_by("id")

        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[0].text, text)
        self.assertEqual(notes[0].page, page)

    def test_post_note_form_valid_assert_return_200(self):
        """ Test if the method return a 200 response if the form is valid. """
        response = self.client.post(
            self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 200)

    def test_post_note_view_text_empty_assert_raise_invalid_form_data(self):
        """ Test if the view return a HttpInvalidFormData if the text is empty. """
        self.form_data["text"] = ""
        self.request = self.factory.post(self.url, self.form_data)
        self.request.user = self.user
        with self.assertRaises(HttpInvalidFormData):
            post_note(self.request, self.codex)

    def test_post_note_codex_not_exist_assert_raise_invalid_form_data(self):
        """ Test if the view return a 404 error if the given slug does not exist. """
        self.url = reverse("notes", kwargs={"codex_slug": "SLUG-NOT-EXISTS"})
        response = self.client.post(
            self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response, HttpResponse)

    def test_post_note_of_other_user_assert_raise_forbidden(self):
        """ Test if the method raise a HttpForbidden error the user has no right to update it. """
        user = User.objects.create_user(
            username="tartine", email="tarnite@lelapin.com", password="top_secret"
        )
        self.request.user = user
        with self.assertRaises(HttpForbidden):
            post_note(self.request, self.codex)

    def test_delete_note_assert_return_405(self):
        """ Test if the view return a 405 response to a not ajax request. """
        response = self.client.delete(
            self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 405)

    def test_post_not_ajax_assert_return_405(self):
        """ Test if the view return a 405 response to a delete request. """
        response = self.client.delete(self.url, self.form_data)

        self.assertEqual(response.status_code, 405)

    def test_post_note_view_not_connected_assert_return_connexion_page(self):
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


class PutNoteTest(TestCase):
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
        self.text = "Test text"
        self.note = Note.objects.create(page=self.page, text=self.text)
        self.url = reverse("note_details", kwargs={"note_id": self.note.id})

        self.form_text = "Updated test text"
        self.form_hash = str(java_string_hashcode(self.text))
        self.form_data = {"text": self.form_text, "hash": self.form_hash}
        self.request = self.factory.post(self.url, self.form_data)
        print(self.request.POST)
        self.request.user = self.user
        self.request.method = "PUT"
        self.request.PUT = self.request.POST

    def test_put_note_assert_return_http_response(self):
        """ Test if the method return a JsonResponse. """
        response = put_note(self.request, self.note)

        self.assertIsInstance(response, JsonResponse)

    def test_put_note_form_valid_assert_note_updated(self):
        """ Test if the model is updated if the input data are valid. """
        put_note(self.request, self.note)

        note = Note.objects.get(id=self.note.id)

        self.assertEqual(note.text, self.form_text)

    def test_put_note_assert_other_note_not_updated(self):
        """ Test if the method does not update other model. """
        codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        page = Page.objects.create(codex=codex)
        text = "Test Text2"
        Note.objects.create(page=page, text=text)
        put_note(self.request, self.note)

        notes = Note.objects.all().order_by("id")

        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[1].text, text)
        self.assertEqual(notes[1].page, page)

    def test_put_note_form_valid_assert_return_200(self):
        """ Test if the method return a 200 response if the form is valid. """
        response = self.client.put(
            self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 200)

    def test_put_note_text_empty_assert_raise_invalid_form_data(self):
        """ Test if the method raise a HttpInvalidFormData error if the form text is empty. """
        self.form_data["text"] = ""
        self.request = self.factory.post(self.url, self.form_data)
        print(self.request.POST)
        self.request.user = self.user
        self.request.method = "PUT"
        self.request.PUT = self.request.POST
        with self.assertRaises(HttpInvalidFormData):
            put_note(self.request, self.note)

    def test_put_note_hash_invalid_assert_raise_invalid_form_data(self):
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
            put_note(self.request, self.note)

    def test_put_note_not_exist_assert_return_http_not_found(self):
        """ Test if the view return a 404 error if the given information does not exist. """
        self.note.delete()
        response = self.client.put(
            self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response, JsonResponse)

    def test_put_note_of_other_user_assert_raise_forbidden(self):
        """ Test if the method raise a HttpForbidden error the user has no right to update it. """
        self.user = User.objects.create_user(
            username="tartine", email="tarnite@lelapin.com", password="top_secret"
        )
        self.request.user = self.user
        with self.assertRaises(HttpForbidden):
            put_note(self.request, self.note)

    def test_put_note_without_form_assert_input_invalid(self):
        """ Test if the view return a 400 response if there is not input form."""
        response = self.client.put(self.url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.assertEqual(response.status_code, 400)

    def test_post_note_assert_return_405(self):
        """ Test if the view return a 405 response to a post request. """
        response = self.client.post(
            self.url, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 405)

    def test_put_note_not_ajax_assert_return_405(self):
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


class DeleteNoteTest(TestCase):
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
        self.note = Note.objects.create(page=self.page, text=self.text)
        self.url = reverse("note_details", kwargs={"note_id": self.note.id})
        self.request = self.factory.delete(self.url)
        self.request.user = self.user

    def test_delete_note_assert_return_json_response(self):
        """ Test if the method return a JsonResponse. """
        response = delete_note(self.request, self.note)

        self.assertIsInstance(response, JsonResponse)

    def test_delete_note_assert_note_deleted(self):
        """ Test if the model is deleted if the input data are valid. """
        delete_note(self.request, self.note)

        note = Note.objects.all()

        self.assertEqual(len(note), 0)

    def test_delete_note_assert_other_note_not_deleted(self):
        """ Test if the method does not delete other model. """
        codex = Codex.objects.create(
            title="Test Codex 2", author=self.user, description="Description 2"
        )
        page = Page.objects.create(codex=codex)
        text = "Test Text2"
        Note.objects.create(page=page, text=text)
        delete_note(self.request, self.note)
        notes = Note.objects.all()

        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].page, page)
        self.assertEqual(notes[0].text, text)

    def test_delete_note_assert_return_200(self):
        """ Test if the view return a 200 response if the form is valid. """
        response = self.client.delete(self.url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.assertEqual(response.status_code, 200)

    def test_delete_note_of_other_user_assert_raise_forbidden(self):
        """ Test if the method raise a HttpForbidden error if the user is not the creator. """
        user = User.objects.create_user(
            username="tartine", email="tarnite@lelapin.com", password="top_secret"
        )
        self.request.user = user
        with self.assertRaises(HttpForbidden):
            delete_note(self.request, self.note)

    def test_post_note_assert_return_405(self):
        """ Test if the view return a 405 response to a put request. """
        response = self.client.post(self.url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.assertEqual(response.status_code, 405)

    def test_delete_not_ajax_assert_return_405(self):
        """ Test if the view return a 405 response to a non ajax request. """
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 405)

    def test_delete_note_view_not_connected_assert_return_connexion_page(self):
        """ Test if a un-connected user can list the notes """
        self.client.logout()
        response = self.client.delete(self.url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.assertRedirects(
            response,
            "/connexion" + "?next=" + self.url,
            status_code=302,
            target_status_code=200,
        )
