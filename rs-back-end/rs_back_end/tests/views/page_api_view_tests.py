from django.urls import reverse
from rest_framework import status

from rs_back_end.commun.utils import java_string_hashcode
from rs_back_end.models import Codex, Page, Note, Task
from rs_back_end.tests.views.defaultAPITestCase import DefaultAPITestCase


class PageGetListViewTest(DefaultAPITestCase):
  def setUp(self):
    self.connect_default_user()
    self.codex1 = Codex.objects.create(
      title="Test Codex 1", author=self.default_user, description="Description 1"
    )
    self.page1 = Page.objects.create(codex=self.codex1)
    self.note1 = Note.objects.create(page=self.page1, text="Test Note 1")
    self.task1 = Task.objects.create(page=self.page1, text="Test Task 1")
    self.task2 = Task.objects.create(page=self.page1, text="Test Task 2")
    self.codex2 = Codex.objects.create(
      title="Test Codex 2", author=self.default_user, description="Description 2"
    )
    self.page2 = Page.objects.create(codex=self.codex2)
    self.note2 = Note.objects.create(page=self.page2, text="Test Note 2")
    self.task3 = Task.objects.create(page=self.page2, text="Test Task 3")
    self.url = reverse("page-list")

  def test_get_list_page_assert_return_http_200(self):
    """ Test if the view return a 200 Response """
    response = self.client.get(self.url)

    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_get_list_page_assert_return_list(self):
    """ Test if the view return a list of page """
    response = self.client.get(self.url)

    self.assertEqual(len(response.data), 2)

    self.assertEqual(response.data[0]["id"], self.page1.id)
    self.assertEqual(response.data[0]["codex"], self.codex1.id)
    self.assertEqual(
      response.data[0]["creation_date"],
      self.page1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[0]["date"],
      self.page1.date.strftime("%Y-%m-%d"),
    )
    self.assertEqual(
      response.data[0]["nested_update_date"],
      self.page1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

    self.assertEqual(response.data[0]["note"]["id"], self.note1.id)
    self.assertEqual(response.data[0]["note"]["page"], self.page1.id)
    self.assertEqual(response.data[0]["note"]["text"], self.note1.text)
    self.assertEqual(
      response.data[0]["note"]["initial_hash"],
      java_string_hashcode(self.note1.text),
    )
    self.assertEqual(
      response.data[0]["note"]["creation_date"],
      self.note1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[0]["note"]["update_date"],
      self.note1.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

    self.assertEqual(len(response.data[0]["tasks"]), 2)

    self.assertEqual(response.data[0]["tasks"][0]["id"], self.task1.id)
    self.assertEqual(response.data[0]["tasks"][0]["page"], self.page1.id)
    self.assertEqual(response.data[0]["tasks"][0]["text"], self.task1.text)
    self.assertEqual(response.data[0]["tasks"][0]["is_achieved"], self.task1.is_achieved)
    self.assertEqual(
      response.data[0]["tasks"][0]["initial_hash"],
      java_string_hashcode(self.task1.text),
    )
    self.assertIsNone(response.data[0]["tasks"][0]["achieved_date"])
    self.assertEqual(
      response.data[0]["tasks"][0]["creation_date"],
      self.task1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[0]["tasks"][0]["update_date"],
      self.task1.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(response.data[0]["tasks"][1]["id"], self.task2.id)
    self.assertEqual(response.data[0]["tasks"][1]["page"], self.page1.id)
    self.assertEqual(response.data[0]["tasks"][1]["text"], self.task2.text)
    self.assertEqual(response.data[0]["tasks"][1]["is_achieved"], self.task2.is_achieved)
    self.assertEqual(
      response.data[0]["tasks"][1]["initial_hash"],
      java_string_hashcode(self.task2.text),
    )
    self.assertIsNone(response.data[0]["tasks"][1]["achieved_date"])
    self.assertEqual(
      response.data[0]["tasks"][1]["creation_date"],
      self.task2.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[0]["tasks"][1]["update_date"],
      self.task2.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

    self.assertEqual(response.data[1]["id"], self.page2.id)
    self.assertEqual(response.data[1]["codex"], self.codex2.id)
    self.assertEqual(
      response.data[1]["creation_date"],
      self.page2.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[1]["date"],
      self.page2.date.strftime("%Y-%m-%d"),
    )
    self.assertEqual(
      response.data[1]["nested_update_date"],
      self.page2.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

    self.assertEqual(response.data[1]["note"]["id"], self.note2.id)
    self.assertEqual(response.data[1]["note"]["page"], self.page2.id)
    self.assertEqual(response.data[1]["note"]["text"], self.note2.text)
    self.assertEqual(
      response.data[1]["note"]["initial_hash"],
      java_string_hashcode(self.note2.text),
    )
    self.assertEqual(
      response.data[1]["note"]["creation_date"],
      self.note2.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[1]["note"]["update_date"],
      self.note2.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

    self.assertEqual(len(response.data[1]["tasks"]), 1)

    self.assertEqual(response.data[1]["tasks"][0]["id"], self.task3.id)
    self.assertEqual(response.data[1]["tasks"][0]["page"], self.page2.id)
    self.assertEqual(response.data[1]["tasks"][0]["text"], self.task3.text)
    self.assertEqual(response.data[1]["tasks"][0]["is_achieved"], self.task3.is_achieved)
    self.assertEqual(
      response.data[1]["tasks"][0]["initial_hash"],
      java_string_hashcode(self.task3.text),
    )
    self.assertIsNone(response.data[1]["tasks"][0]["achieved_date"])
    self.assertEqual(
      response.data[1]["tasks"][0]["creation_date"],
      self.task3.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[1]["tasks"][0]["update_date"],
      self.task3.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

  def test_get_filtered_list_page_assert_return_list(self):
    """ Test if the view return a list of filtered page """
    response = self.client.get(self.url + "?codex__slug=" + self.codex1.slug)

    self.assertEqual(len(response.data), 1)

    self.assertEqual(response.data[0]["id"], self.page1.id)
    self.assertEqual(response.data[0]["codex"], self.codex1.id)
    self.assertEqual(
      response.data[0]["creation_date"],
      self.page1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[0]["date"],
      self.page1.date.strftime("%Y-%m-%d"),
    )
    self.assertEqual(
      response.data[0]["nested_update_date"],
      self.page1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

    self.assertEqual(response.data[0]["note"]["id"], self.note1.id)
    self.assertEqual(response.data[0]["note"]["page"], self.page1.id)
    self.assertEqual(response.data[0]["note"]["text"], self.note1.text)
    self.assertEqual(
      response.data[0]["note"]["initial_hash"],
      java_string_hashcode(self.note1.text),
    )
    self.assertEqual(
      response.data[0]["note"]["creation_date"],
      self.note1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[0]["note"]["update_date"],
      self.note1.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

    self.assertEqual(len(response.data[0]["tasks"]), 2)

    self.assertEqual(response.data[0]["tasks"][0]["id"], self.task1.id)
    self.assertEqual(response.data[0]["tasks"][0]["page"], self.page1.id)
    self.assertEqual(response.data[0]["tasks"][0]["text"], self.task1.text)
    self.assertEqual(response.data[0]["tasks"][0]["is_achieved"], self.task1.is_achieved)
    self.assertEqual(
      response.data[0]["tasks"][0]["initial_hash"],
      java_string_hashcode(self.task1.text),
    )
    self.assertIsNone(response.data[0]["tasks"][0]["achieved_date"])
    self.assertEqual(
      response.data[0]["tasks"][0]["creation_date"],
      self.task1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[0]["tasks"][0]["update_date"],
      self.task1.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(response.data[0]["tasks"][1]["id"], self.task2.id)
    self.assertEqual(response.data[0]["tasks"][1]["page"], self.page1.id)
    self.assertEqual(response.data[0]["tasks"][1]["text"], self.task2.text)
    self.assertEqual(response.data[0]["tasks"][1]["is_achieved"], self.task2.is_achieved)
    self.assertEqual(
      response.data[0]["tasks"][1]["initial_hash"],
      java_string_hashcode(self.task2.text),
    )
    self.assertIsNone(response.data[0]["tasks"][1]["achieved_date"])
    self.assertEqual(
      response.data[0]["tasks"][1]["creation_date"],
      self.task2.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[0]["tasks"][1]["update_date"],
      self.task2.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

  def test_get_list_page_not_codex_author_return_only_self_codex(self):
    """ Test if a user can list page of other user """
    other_user_name = "oz"
    self.connect_user(other_user_name)
    codex3 = Codex.objects.create(
      title="Test Codex 3", author=self.users[other_user_name], description="Description 3"
    )
    page3 = Page.objects.create(codex=codex3)
    note3 = Note.objects.create(page=page3, text="Test Note 3")

    response = self.client.get(self.url)

    self.assertEqual(len(response.data), 1)

    self.assertEqual(response.data[0]["id"], page3.id)
    self.assertEqual(response.data[0]["codex"], codex3.id)
    self.assertEqual(
      response.data[0]["creation_date"],
      page3.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[0]["date"],
      page3.date.strftime("%Y-%m-%d"),
    )
    self.assertEqual(
      response.data[0]["nested_update_date"],
      page3.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

    self.assertEqual(response.data[0]["note"]["id"], note3.id)
    self.assertEqual(response.data[0]["note"]["page"], page3.id)
    self.assertEqual(response.data[0]["note"]["text"], note3.text)
    self.assertEqual(
      response.data[0]["note"]["initial_hash"],
      java_string_hashcode(note3.text),
    )
    self.assertEqual(
      response.data[0]["note"]["creation_date"],
      note3.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[0]["note"]["update_date"],
      note3.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

  def test_get_list_page_not_connected_return_401(self):
    """ Test if a un-connected user can list page """
    self.client.logout()
    response = self.client.get(self.url)

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PageGetDetailViewTest(DefaultAPITestCase):
  def setUp(self):
    self.connect_default_user()
    self.codex1 = Codex.objects.create(
      title="Test Codex 1", author=self.default_user, description="Description 1"
    )
    self.page1 = Page.objects.create(codex=self.codex1)
    self.note1 = Note.objects.create(page=self.page1, text="Test Note 1")
    self.task1 = Task.objects.create(page=self.page1, text="Test Task 1")
    self.task2 = Task.objects.create(page=self.page1, text="Test Task 2")
    self.url = reverse("page-detail", args=[1])

  def test_get_detail_page_assert_return_http_200(self):
    """ Test if the view return a 200 Response """
    response = self.client.get(self.url)

    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_get_detail_page_assert_return_codex(self):
    """ Test if the view return a unique page """
    response = self.client.get(self.url)

    self.assertEqual(len(response.data), 7)

    self.assertEqual(response.data["id"], self.page1.id)
    self.assertEqual(response.data["codex"], self.codex1.id)
    self.assertEqual(
      response.data["creation_date"],
      self.page1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data["date"],
      self.page1.date.strftime("%Y-%m-%d"),
    )
    self.assertEqual(
      response.data["nested_update_date"],
      self.task2.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

    self.assertEqual(response.data["note"]["id"], self.note1.id)
    self.assertEqual(response.data["note"]["page"], self.page1.id)
    self.assertEqual(response.data["note"]["text"], self.note1.text)
    self.assertEqual(
      response.data["note"]["initial_hash"],
      java_string_hashcode(self.note1.text),
    )
    self.assertEqual(
      response.data["note"]["creation_date"],
      self.note1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data["note"]["update_date"],
      self.note1.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

    self.assertEqual(len(response.data["tasks"]), 2)

    self.assertEqual(response.data["tasks"][0]["id"], self.task1.id)
    self.assertEqual(response.data["tasks"][0]["page"], self.page1.id)
    self.assertEqual(response.data["tasks"][0]["text"], self.task1.text)
    self.assertEqual(response.data["tasks"][0]["is_achieved"], self.task1.is_achieved)
    self.assertEqual(
      response.data["tasks"][0]["initial_hash"],
      java_string_hashcode(self.task1.text),
    )
    self.assertIsNone(response.data["tasks"][0]["achieved_date"])
    self.assertEqual(
      response.data["tasks"][0]["creation_date"],
      self.task1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data["tasks"][0]["update_date"],
      self.task1.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(response.data["tasks"][1]["id"], self.task2.id)
    self.assertEqual(response.data["tasks"][1]["page"], self.page1.id)
    self.assertEqual(response.data["tasks"][1]["text"], self.task2.text)
    self.assertEqual(response.data["tasks"][1]["is_achieved"], self.task2.is_achieved)
    self.assertEqual(
      response.data["tasks"][1]["initial_hash"],
      java_string_hashcode(self.task2.text),
    )
    self.assertIsNone(response.data["tasks"][1]["achieved_date"])
    self.assertEqual(
      response.data["tasks"][1]["creation_date"],
      self.task2.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data["tasks"][1]["update_date"],
      self.task2.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

  def test_get_detail_page_not_exist_assert_return_http_404(self):
    """ Test if the view return a 404 Response if the page does not exist """
    response = self.client.get(reverse("page-detail", args=[2]))

    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_get_detail_page_of_other_user_assert_return_http_404(self):
    """ Test if the view return a 404 Response when trying to retrieve an other user page """
    self.connect_user("oz")
    response = self.client.get(self.url)

    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_get_detail_page_user_not_connected_return_401(self):
    """ Test if a un-connected user can retrieve a page """
    self.client.logout()
    response = self.client.get(self.url)

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PagePostViewTest(DefaultAPITestCase):
  def setUp(self):
    self.connect_default_user()
    self.url = reverse("page-list")

  def test_post_page_assert_return_http_405(self):
    """ Test if the view return a 405 Response """
    response = self.client.post(self.url)

    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class PagePutViewTest(DefaultAPITestCase):
  def setUp(self):
    self.connect_default_user()
    self.url = reverse("page-detail", args=[1])

  def test_put_page_assert_return_http_405(self):
    """ Test if the view return a 405 Response """
    response = self.client.put(self.url)

    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class PageDeleteViewTest(DefaultAPITestCase):
  def setUp(self):
    self.connect_default_user()
    self.url = reverse("page-detail", args=[1])

  def test_delete_page_assert_return_http_405(self):
    """ Test if the view return a 405 Response """
    response = self.client.delete(self.url)

    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
