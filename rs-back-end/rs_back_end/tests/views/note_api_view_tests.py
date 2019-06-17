from django.urls import reverse
from rest_framework import status

from rs_back_end.commun.utils import java_string_hashcode
from rs_back_end.models import Codex, Page, Note
from rs_back_end.tests.views.defaultAPITestCase import DefaultAPITestCase


class NoteGetListViewTest(DefaultAPITestCase):
  def setUp(self):
    self.connect_default_user()
    self.codex1 = Codex.objects.create(
      title="Test Codex 1", author=self.default_user, description="Description 1"
    )
    self.page1 = Page.objects.create(codex=self.codex1)
    self.note1 = Note.objects.create(page=self.page1, text="Test Note 1")
    self.codex2 = Codex.objects.create(
      title="Test Codex 2", author=self.default_user, description="Description 2"
    )
    self.page2 = Page.objects.create(codex=self.codex2)
    self.note2 = Note.objects.create(page=self.page2, text="Test Note 2")
    self.url = reverse("note-list")

  def test_get_list_note_assert_return_http_200(self):
    """ Test if the view return a 200 Response """
    response = self.client.get(self.url)

    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_get_list_note_assert_return_list(self):
    """ Test if the view return a list of note """
    response = self.client.get(self.url)

    self.assertEqual(len(response.data), 2)

    self.assertEqual(response.data[0]["id"], self.note1.id)
    self.assertEqual(response.data[0]["page"], self.page1.id)
    self.assertEqual(response.data[0]["text"], self.note1.text)
    self.assertEqual(
      response.data[0]["initial_hash"],
      java_string_hashcode(self.note1.text),
    )
    self.assertEqual(
      response.data[0]["creation_date"],
      self.note1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[0]["update_date"],
      self.note1.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

    self.assertEqual(response.data[1]["id"], self.note2.id)
    self.assertEqual(response.data[1]["page"], self.page2.id)
    self.assertEqual(response.data[1]["text"], self.note2.text)
    self.assertEqual(
      response.data[1]["initial_hash"],
      java_string_hashcode(self.note2.text),
    )
    self.assertEqual(
      response.data[1]["creation_date"],
      self.note2.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[1]["update_date"],
      self.note2.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

  def test_get_filtered_list_note_assert_return_list(self):
    """ Test if the view return a list of filtered note """
    response = self.client.get(self.url + "?page__codex__slug=" + self.codex1.slug)

    self.assertEqual(len(response.data), 1)

    self.assertEqual(response.data[0]["id"], self.note1.id)
    self.assertEqual(response.data[0]["page"], self.page1.id)
    self.assertEqual(response.data[0]["text"], self.note1.text)
    self.assertEqual(
      response.data[0]["initial_hash"],
      java_string_hashcode(self.note1.text),
    )
    self.assertEqual(
      response.data[0]["creation_date"],
      self.note1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[0]["update_date"],
      self.note1.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

  def test_get_list_note_not_codex_author_return_only_self_codex(self):
    """ Test if a user can list note of other user """
    other_user_name = "oz"
    self.connect_user(other_user_name)
    codex3 = Codex.objects.create(
      title="Test Codex 3", author=self.users[other_user_name], description="Description 3"
    )
    page3 = Page.objects.create(codex=codex3)
    note3 = Note.objects.create(page=page3, text="Test Note 3")

    response = self.client.get(self.url)

    self.assertEqual(len(response.data), 1)

    self.assertEqual(response.data[0]["id"], note3.id)
    self.assertEqual(response.data[0]["page"], page3.id)
    self.assertEqual(response.data[0]["text"], note3.text)
    self.assertEqual(
      response.data[0]["initial_hash"],
      java_string_hashcode(note3.text),
    )
    self.assertEqual(
      response.data[0]["creation_date"],
      note3.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[0]["update_date"],
      note3.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

  def test_get_list_note_not_connected_return_401(self):
    """ Test if a un-connected user can list note """
    self.client.logout()
    response = self.client.get(self.url)

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class NoteGetDetailViewTest(DefaultAPITestCase):
  def setUp(self):
    self.connect_default_user()
    self.codex = Codex.objects.create(
      title="Test Codex 1", author=self.default_user, description="Description 1"
    )
    self.page = Page.objects.create(codex=self.codex)
    self.note = Note.objects.create(page=self.page, text="Test Note 1")
    self.url = reverse("note-detail", args=[1])

  def test_get_detail_note_assert_return_http_200(self):
    """ Test if the view return a 200 Response """
    response = self.client.get(self.url)

    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_get_detail_note_assert_return_codex(self):
    """ Test if the view return a unique note """
    response = self.client.get(self.url)

    self.assertEqual(len(response.data), 6)

    self.assertEqual(response.data["id"], self.note.id)
    self.assertEqual(response.data["page"], self.page.id)
    self.assertEqual(response.data["text"], self.note.text)
    self.assertEqual(
      response.data["initial_hash"],
      java_string_hashcode(self.note.text),
    )
    self.assertEqual(
      response.data["creation_date"],
      self.note.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data["update_date"],
      self.note.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

  def test_get_detail_note_not_exist_assert_return_http_404(self):
    """ Test if the view return a 404 Response if the note does not exist """
    response = self.client.get(reverse("note-detail", args=[2]))

    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_get_detail_note_of_other_user_assert_return_http_404(self):
    """ Test if the view return a 404 Response when trying to retrieve an other user note """
    self.connect_user("oz")
    response = self.client.get(self.url)

    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_get_detail_note_user_not_connected_return_401(self):
    """ Test if a un-connected user can retrieve a note """
    self.client.logout()
    response = self.client.get(self.url)

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class NotePostViewTest(DefaultAPITestCase):
  def setUp(self):
    self.connect_default_user()
    self.codex1 = Codex.objects.create(
      title="Test Codex 1", author=self.default_user, description="Description 1"
    )
    self.page1 = Page.objects.create(codex=self.codex1)
    self.note1 = Note.objects.create(page=self.page1, text="Test Note 1")
    self.codex2 = Codex.objects.create(
      title="Test Codex 2", author=self.default_user, description="Description 2"
    )
    self.url = reverse("note-list")
    self.slug = "test-codex-2"
    self.data = {"codex": "2", "text": "Text 2"}

  def test_post_note_assert_return_http_201(self):
    """ Test if the view return a 201 Response """
    response = self.client.post(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  def test_post_note_text_missing_assert_return_http_400(self):
    """ Test if the view return a 400 Response if the text is missing """
    self.data.pop("text")
    response = self.client.post(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data["text"][0], "This field is required.")

  def test_post_note_codex_missing_assert_return_http_400(self):
    """ Test if the view return a 400 Response if the codex id is missing """
    self.data.pop("codex")
    response = self.client.post(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data["codex"][0], "This field is required.")

  def test_post_note_codex_not_exist_assert_return_http_400(self):
    """ Test if the view return a 400 Response if the codex does not exist """
    self.data["codex"] = "3"
    response = self.client.post(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data["codex"][0], "The specified Codex does not exist.")

  def test_post_note_assert_return_note(self):
    """ Test if the view return an note """
    response = self.client.post(self.url, self.data)

    self.assertEqual(len(response.data), 6)

    self.assertEqual(response.data["id"], 2)
    self.assertEqual(response.data["page"], 2)
    self.assertEqual(response.data["text"], self.data["text"])
    self.assertEqual(response.data["initial_hash"], java_string_hashcode(self.data["text"]))
    self.assertIsNotNone(response.data["creation_date"])
    self.assertIsNotNone(response.data["update_date"])

  def test_post_note_assert_create_note(self):
    """ Test if the note is created in the data base """
    self.client.post(self.url, self.data)
    note_list = Note.objects.all()
    new_note = Note.objects.filter(id=2)

    self.assertEqual(len(note_list), 2)
    self.assertEqual(len(new_note), 1)
    self.assertEqual(new_note[0].page.codex.id, int(self.data["codex"]))
    self.assertEqual(new_note[0].text, self.data["text"])

  def test_post_note_assert_user_has_permissions(self):
    """ Test if the note is created with the correct permissions.py """
    self.client.post(self.url, self.data)
    note = Note.objects.get(id=2)

    self.assertEqual(self.default_user.has_perm('view_note', note), True)
    self.assertEqual(self.default_user.has_perm('change_note', note), True)
    self.assertEqual(self.default_user.has_perm('delete_note', note), True)

  def test_post_note_already_exist_assert_return_http_400(self):
    """ Test if the view return a 400 response if the note already exist """
    self.data["codex"] = "1"
    response = self.client.post(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(
      response.data['non_field_errors'][0], 'The Note of the day already exist for this Codex.'
    )

  def test_post_note_user_not_codex_owner_assert_return_http_403(self):
    """ Test if a user can create a note for a un-owned codex """
    self.connect_user("oz")
    response = self.client.post(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

  def test_post_note_user_not_connected_assert_return_http_401(self):
    """ Test if a un-connected user can create a Note """
    self.client.logout()
    response = self.client.post(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class NotePutViewTest(DefaultAPITestCase):
  def setUp(self):
    self.connect_default_user()
    self.codex1 = Codex.objects.create(
      title="Test Codex 1", author=self.default_user, description="Description 1"
    )
    self.page1 = Page.objects.create(codex=self.codex1)
    self.note1 = Note.objects.create(text="Test note 1", page=self.page1)
    self.codex2 = Codex.objects.create(
      title="Test Codex 2", author=self.default_user, description="Description 2"
    )
    self.page2 = Page.objects.create(codex=self.codex2)
    self.note2 = Note.objects.create(text="Test note 2", page=self.page2)
    self.url = reverse("note-detail", args=[1])
    self.data = {
      "text": "Test note 1 updated",
      "modification_hash": java_string_hashcode(self.note1.text),
    }

  def test_put_note_assert_return_http_200(self):
    """ Test if the view return a 200 Response """
    response = self.client.put(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_put_note_text_missing_assert_return_http_400(self):
    """ Test if the view return a 400 Response if the text is missing """
    self.data.pop("text")
    response = self.client.put(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data["text"][0], "This field is required.")

  def test_put_note_hash_missing_assert_return_http_400(self):
    """ Test if the view return a 400 Response if the hash is missing """
    self.data.pop("modification_hash")
    response = self.client.put(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(
      response.data["modification_hash"][0], "This field is required."
    )

  def test_put_note_hash_wrong_assert_return_http_400(self):
    """ Test if the view return a 400 Response if the hash is wrong """
    self.data["modification_hash"] = 0
    response = self.client.put(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(
      response.data["modification_hash"][0],
      "The Note have been modified since the last "
      "modification attempt.",
    )

  def test_put_note_assert_return_note(self):
    """ Test if the view return an note """
    response = self.client.put(self.url, self.data)

    self.assertEqual(len(response.data), 6)

    self.assertEqual(response.data["id"], self.note1.id)
    self.assertEqual(response.data["page"], self.page1.id)
    self.assertEqual(response.data["text"], self.data["text"])
    self.assertEqual(response.data["initial_hash"], java_string_hashcode(self.data["text"]))
    self.assertEqual(
      response.data["creation_date"],
      self.note1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    self.assertIsNotNone(response.data["update_date"])

  def test_put_note_assert_note_updated(self):
    """ Test if the note is updated in the data base """
    self.client.put(self.url, self.data)
    note_list = Note.objects.all()
    updated_note = Note.objects.filter(id=1)

    self.assertEqual(len(note_list), 2)
    self.assertEqual(len(updated_note), 1)
    self.assertEqual(updated_note[0].text, self.data["text"])

  def test_put_note_assert_other_note_not_updated(self):
    """ Test if other note are not updated in the data base """
    self.client.put(self.url, self.data)
    note2 = Note.objects.get(id=2)

    self.assertNotEqual(note2.text, self.data["text"])

  def test_put_note_not_exist_assert_return_http_404(self):
    """ Test if the view return a 404 Response if the note does not exist """
    response = self.client.put(reverse("note-detail", args=[3]), self.data)

    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_put_note_of_other_user_assert_return_http_404(self):
    """ Test if the view return a 404 Response when trying to update an other user codex """
    self.connect_user("oz")
    response = self.client.put(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_put_codex_not_connected_return_401(self):
    """ Test if a un-connected user can update a Codex """
    self.client.logout()
    response = self.client.put(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class NoteDeleteViewTest(DefaultAPITestCase):
  def setUp(self):
    self.connect_default_user()
    self.codex1 = Codex.objects.create(
      title="Test Codex 1", author=self.default_user, description="Description 1"
    )
    self.page1 = Page.objects.create(codex=self.codex1)
    self.note1 = Note.objects.create(page=self.page1, text="Test Note 1")
    self.codex2 = Codex.objects.create(
      title="Test Codex 2", author=self.default_user, description="Description 2"
    )
    self.page2 = Page.objects.create(codex=self.codex2)
    self.note2 = Note.objects.create(page=self.page2, text="Test Note 2")
    self.url = reverse("note-detail", args=[1])

  def test_delete_note_assert_return_http_204(self):
    """ Test if the view return a 204 Response """
    response = self.client.delete(self.url)

    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

  def test_delete_note_not_exist_assert_return_http_400(self):
    """ Test if the view return a 400 Response if the note does not exist """
    response = self.client.delete(reverse("note-detail", args=[3]))

    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_delete_note_assert_note_deleted(self):
    """ Test if the note is deleted in the data base """
    self.client.delete(self.url)
    note_list = Note.objects.all()
    new_note = Note.objects.filter(id=1)

    self.assertEqual(len(note_list), 1)

    self.assertEqual(len(new_note), 0)

  def test_delete_note_of_other_user_assert_return_http_404(self):
    """ Test if the view return a 404 Response when trying to delete an other user note """
    self.connect_user("oz")
    response = self.client.delete(self.url)

    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_delete_note_user_not_connected_assert_return_http_401(self):
    """ Test if a un-connected user can create an note """
    self.client.logout()
    response = self.client.delete(self.url)

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
