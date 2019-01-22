from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.urls import reverse

from projets.commun.error import HttpForbidden, HttpInvalidFormData
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


class NoteViewTest(TestCase):
    def setUp(self):
        self.text = "Test Text"
        self.user = User.objects.create_user(
            username="zamour", email="zamour@zamour.com", password="top_secret"
        )
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        self.page = Page.objects.create(codex=self.codex)
        self.note = Note.objects.create(page=self.page, text=self.text)

    def test_is_authorized_to_create_note_user_is_author_note_assert_return_true(self):
        is_authorized = is_authorized_to_create_note(self.user, self.codex)

        self.assertEqual(is_authorized, True)

    def test_is_authorized_to_create_note_user_is_not_author_note_assert_return_false(
        self
    ):
        user = self.user = User.objects.create_user(
            username="test_user", email="test_user@test.com", password="admin"
        )
        is_authorized = is_authorized_to_create_note(user, self.codex)

        self.assertEqual(is_authorized, False)

    def test_is_authorized_to_update_note_user_is_author_note_assert_return_true(self):
        is_authorized = is_authorized_to_update_note(self.user, self.note)

        self.assertEqual(is_authorized, True)

    def test_is_authorized_to_update_note_user_is_not_author_note_assert_return_false(
        self
    ):
        user = self.user = User.objects.create_user(
            username="test_user", email="test_user@test.com", password="admin"
        )
        is_authorized = is_authorized_to_update_note(user, self.note)

        self.assertEqual(is_authorized, False)

    def test_is_authorized_to_delete_note_user_is_author_note_assert_return_true(self):
        is_authorized = is_authorized_to_delete_note(self.user, self.note.id)

        self.assertEqual(is_authorized, True)

    def test_is_authorized_to_delete_note_user_is_not_author_note_assert_return_false(
        self
    ):
        user = self.user = User.objects.create_user(
            username="test_user", email="test_user@test.com", password="admin"
        )
        is_authorized = is_authorized_to_delete_note(user, self.note.id)

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
        self.page = Page.objects.create(codex=self.codex)
        self.url_list = reverse("notes")
        self.form_text = "Test Text"
        self.form_is_achieved = True
        self.form_data = {"text": self.form_text, "codex_slug": self.codex.slug}

    def test_post_note_assert_return_http_response(self):
        """ Test if the method return a HttpResponse """
        request = self.factory.post(self.url_list, self.form_data)
        request.user = self.user
        response = post_note(request)

        self.assertIsInstance(response, HttpResponse)

    def test_post_note_assert_note_created(self):
        """ Test if the method create the given note """
        request = self.factory.post(self.url_list, self.form_data)
        request.user = self.user
        post_note(request)
        note = Note.objects.get(text=self.form_text)

        self.assertEqual(note.text, self.form_text)

    def test_post_note_already_exist_assert_raise_invalid_form_data(self):
        """ Test if the method return an HttpInvalidFormData if the note of the day already exist """
        Note.objects.create(page=self.page, text=self.form_text)
        request = self.factory.post(self.url_list, self.form_data)
        request.user = self.user
        with self.assertRaises(HttpInvalidFormData):
            post_note(request)

    def test_post_note_assert_other_note_not_updated(self):
        """ Test if the method does not update other note """
        codex = Codex.objects.create(
            title="Test Codex 2", author=self.user, description="Description 2"
        )
        page = Page.objects.create(codex=codex)
        text = "No update test text"
        Note.objects.create(page=page, text=text)
        request = self.factory.post(self.url_list, self.form_data)
        request.user = self.user
        post_note(request)
        notes = Note.objects.all().order_by("id")

        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[0].text, text)

    def test_post_note_view_assert_return_200(self):
        """ Test if the view return a 200 response to a get request"""
        response = self.client.post(
            self.url_list, self.form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 200)

    def test_post_note_view_text_empty_assert_raise_invalid_form_data(self):
        """ Test if the view return a HttpInvalidFormData if the text is empty """
        self.form_data["text"] = ""
        request = self.factory.post(self.url_list, self.form_data)
        request.user = self.user
        with self.assertRaises(HttpInvalidFormData):
            post_note(request)

    def test_post_note_view_without_slug_assert_raise_invalid_form_data(self):
        """ Test if the view return a HttpInvalidFormData if the slug is empty """
        del self.form_data["codex_slug"]
        request = self.factory.post(self.url_list, self.form_data)
        request.user = self.user
        with self.assertRaises(HttpInvalidFormData):
            post_note(request)

    def test_post_note_view_codex_not_exist_assert_raise_invalid_form_data(self):
        """ Test if the view return a HttpInvalidFormData if the given slug does not exist """
        self.form_data["codex_slug"] = "slug-ko"
        request = self.factory.post(self.url_list, self.form_data)
        request.user = self.user
        with self.assertRaises(HttpInvalidFormData):
            post_note(request)

    def test_post_note_of_other_user_assert_raise_forbidden(self):
        """ Test if the method raise a HttpForbidden error the user has no right to update it """
        user = User.objects.create_user(
            username="tartine", email="tarnite@lelapin.com", password="top_secret"
        )
        request = self.factory.post(self.url_list, self.form_data)
        request.user = user
        with self.assertRaises(HttpForbidden):
            post_note(request)

    def test_delete_note_not_ajax_view_assert_return_405(self):
        """ Test if the view return a 405 response to a not ajax request"""
        response = self.client.delete(self.url_list)

        self.assertEqual(response.status_code, 405)

    def test_delete_note_view_assert_return_405(self):
        """ Test if the view return a 405 response to a delete request"""
        response = self.client.delete(
            self.url_list, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 405)

    def test_post_note_view_not_connected_assert_return_connexion_page(self):
        """ Test if a un-connected user can create a note """
        self.client.logout()
        response = self.client.delete(self.url_list)

        self.assertRedirects(
            response,
            "/connexion" + "?next=" + self.url_list,
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
        self.form_text = "Updated Test Text"
        self.form_hash = str(java_string_hashcode(self.text))
        self.form_data = {"text": self.form_text, "hash": self.form_hash}
        self.page = Page.objects.create(codex=self.codex)
        self.note = Note.objects.create(page=self.page, text=self.text)
        self.url_details = reverse("note_details", kwargs={"note_id": self.note.id})

    def test_delete_note_assert_return_http_response(self):
        """ Test if the method return a HttpResponse """
        request = self.factory.delete(self.url_details)
        request.user = self.user
        response = delete_note(request, self.note.id)

        self.assertIsInstance(response, HttpResponse)

    def test_delete_note_assert_delete_note(self):
        """ Test if the method return a HttpResponse """
        request = self.factory.delete(self.url_details)
        request.user = self.user
        note_id = self.note.id
        delete_note(request, note_id)
        note = Note.objects.filter(id=note_id)

        self.assertEqual(len(note), 0)

    def test_delete_note_assert_does_not_delete_other_note(self):
        """ Test if the method return a HttpResponse """
        codex = Codex.objects.create(
            title="Test Codex 2", author=self.user, description="Description 2"
        )
        page = Page.objects.create(codex=codex)
        note2 = Note.objects.create(page=page, text="Test Text2")
        request = self.factory.delete(self.url_details)
        request.user = self.user
        delete_note(request, self.note.id)
        notes = Note.objects.filter(id=note2.id)

        self.assertEqual(len(notes), 1)

    def test_delete_note_of_other_user_assert_raise_forbidden(self):
        """ Test if the method raise a HttpForbidden error if the user is not the creator """
        user = User.objects.create_user(
            username="tartine", email="tarnite@lelapin.com", password="top_secret"
        )
        codex = Codex.objects.create(
            title="Test Codex 2", author=user, description="Description 2"
        )
        page = Page.objects.create(codex=codex)
        note = Note.objects.create(page=page, text="Test Text2")
        request = self.factory.delete(self.url_details)
        request.user = self.user
        with self.assertRaises(HttpForbidden):
            delete_note(request, note.id)

    def test_delete_note_details_view_assert_return_200(self):
        """ Test if the view return a 200 response to a get request"""
        response = self.client.delete(
            self.url_details, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_note_details_view_not_ajax_assert_return_405(self):
        """ Test if the view return a 405 response to a get request"""
        response = self.client.delete(self.url_details)

        self.assertEqual(response.status_code, 405)

    def test_delete_note_view_not_connected_assert_return_connexion_page(self):
        """ Test if a un-connected user can list the notes """
        self.client.logout()
        response = self.client.delete(self.url_details)

        self.assertRedirects(
            response,
            "/connexion" + "?next=" + self.url_details,
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
        self.text = "Test Text"
        self.form_text = "Updated Test Text"
        self.form_hash = str(java_string_hashcode(self.text))
        self.form_data = {"text": self.form_text, "hash": self.form_hash}
        self.page = Page.objects.create(codex=self.codex)
        self.note = Note.objects.create(page=self.page, text=self.text)
        self.url_details = reverse("note_details", kwargs={"note_id": self.note.id})

    def test_put_note_assert_return_http_response(self):
        """ Test if the method return a HttpResponse """
        request = self.factory.post(self.url_details, self.form_data)
        print(request.POST)
        request.user = self.user
        request.method = "PUT"
        request.PUT = request.POST
        response = put_note(request, self.note.id)

        self.assertIsInstance(response, HttpResponse)

    def test_put_note_assert_note_updated(self):
        """ Test if the method update the given note """
        request = self.factory.post(self.url_details, self.form_data)
        print(request.POST)
        request.user = self.user
        request.method = "PUT"
        request.PUT = request.POST
        put_note(request, self.note.id)

        note = Note.objects.get(id=self.note.id)

        self.assertEqual(note.text, self.form_text)

    def test_put_note_assert_other_note_not_updated(self):
        """ Test if the method does not update other note """
        codex = Codex.objects.create(
            title="Test Codex 1", author=self.user, description="Description 1"
        )
        page = Page.objects.create(codex=codex)
        text = "Test Text2"
        note = Note.objects.create(page=page, text=text)
        request = self.factory.post(self.url_details, self.form_data)
        request.user = self.user
        print(request.POST)
        request.method = "PUT"
        request.PUT = request.POST
        put_note(request, self.note.id)

        notes = Note.objects.filter(id=note.id)

        self.assertEqual(notes[0].text, text)

    def test_put_note_text_empty_assert_raise_invalid_form_data(self):
        """ Test if the method raise a HttpInvalidFormData error if the form text is empty """
        self.form_data["text"] = ""
        request = self.factory.post(self.url_details, self.form_data)
        request.user = self.user
        request.method = "PUT"
        print(request.POST)
        request.PUT = request.POST
        with self.assertRaises(HttpInvalidFormData):
            put_note(request, self.note.id)

    def test_put_note_does_not_exist_assert_raise_invalid_form_data(self):
        """ Test if the method raise a HttpInvalidFormData error if the note does not exist """
        request = self.factory.post(self.url_details, self.form_data)
        print(request.POST)
        request.user = self.user
        request.method = "PUT"
        request.PUT = request.POST
        with self.assertRaises(HttpInvalidFormData):
            put_note(request, note_id=0)

    def test_put_note_hash_invalid_assert_raise_invalid_form_data(self):
        """
        Test if the method raise a HttpInvalidFormData error if the text hash is not the same as the one of the
        database text
        """
        self.form_data["hash"] = "1"
        request = self.factory.post(self.url_details, self.form_data)
        print(request.POST)
        request.user = self.user
        request.method = "PUT"
        request.PUT = request.POST
        with self.assertRaises(HttpInvalidFormData):
            put_note(request, self.note.id)

    def test_put_note_of_other_user_assert_raise_forbidden(self):
        """ Test if the method raise a HttpForbidden error the user has no right to update it """
        user = User.objects.create_user(
            username="tartine", email="tarnite@lelapin.com", password="top_secret"
        )
        request = self.factory.post(self.url_details, self.form_data)
        print(request.POST)
        request.user = user
        request.method = "PUT"
        request.PUT = request.POST
        with self.assertRaises(HttpForbidden):
            put_note(request, self.note.id)

    def test_put_note_details_view_assert_input_invalid(self):
        """ Test if the view return a 400 response if there is not form data"""
        response = self.client.put(
            self.url_details, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 400)

    def test_post_note_details_view_assert_return_405(self):
        """ Test if the view return a 405 response to a get request"""
        response = self.client.post(
            self.url_details, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 405)
