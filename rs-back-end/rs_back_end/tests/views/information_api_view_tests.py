from django.urls import reverse
from rest_framework import status

from rs_back_end.commun.utils import java_string_hashcode
from rs_back_end.models import Codex, Information
from rs_back_end.tests.views.defaultAPITestCase import DefaultAPITestCase


class InformationGetListViewTest(DefaultAPITestCase):
  def setUp(self):
    self.connect_default_user()
    self.codex1 = Codex.objects.create(
      title="Test Codex 1", author=self.default_user, description="Description 1"
    )
    self.information1 = Information.objects.create(
      text="Test Information 1", codex=self.codex1
    )
    self.codex2 = Codex.objects.create(
      title="Test Codex 2", author=self.default_user, description="Description 2"
    )
    self.information2 = Information.objects.create(
      text="Test Information 2", codex=self.codex2
    )
    self.default_user.has_perm('rs_back_end.view_information', Information.objects.get(id=1))
    self.url = reverse("information-list")

  def test_get_list_information_assert_return_http_200(self):
    """ Test if the view return a 200 Response """
    response = self.client.get(self.url)

    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_get_list_information_assert_return_list(self):
    """ Test if the view return a list of codex information """
    response = self.client.get(self.url)

    self.assertEqual(len(response.data), 2)

    self.assertEqual(response.data[0]["id"], self.information1.id)
    self.assertEqual(response.data[0]["codex"], self.codex1.id)
    self.assertEqual(response.data[0]["text"], self.information1.text)
    self.assertEqual(
      response.data[0]["initial_hash"],
      java_string_hashcode(self.information1.text),
    )
    self.assertEqual(
      response.data[0]["creation_date"],
      self.information1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[0]["update_date"],
      self.information1.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

    self.assertEqual(response.data[1]["id"], self.information2.id)
    self.assertEqual(response.data[1]["codex"], self.codex2.id)
    self.assertEqual(response.data[1]["text"], self.information2.text)
    self.assertEqual(
      response.data[1]["initial_hash"],
      java_string_hashcode(self.information2.text),
    )
    self.assertEqual(
      response.data[1]["creation_date"],
      self.information2.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[1]["update_date"],
      self.information2.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

  def test_get_filtered_list_information_assert_return_list(self):
    """ Test if the view return a list of filtered codex information """
    response = self.client.get(self.url + "?codex__slug=" + self.codex1.slug)

    self.assertEqual(len(response.data), 1)

    self.assertEqual(response.data[0]["id"], self.information1.id)
    self.assertEqual(response.data[0]["codex"], self.codex1.id)
    self.assertEqual(response.data[0]["text"], self.information1.text)
    self.assertEqual(
      response.data[0]["initial_hash"],
      java_string_hashcode(self.information1.text),
    )
    self.assertEqual(
      response.data[0]["creation_date"],
      self.information1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[0]["update_date"],
      self.information1.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

  def test_get_list_information_not_codex_author_return_only_self_codex(self):
    """ Test if a user can list information of other user """
    other_user_name = "oz"
    self.connect_user(other_user_name)
    codex3 = self.empty_codex = Codex.objects.create(
      title="Test Codex 3", author=self.users[other_user_name], description="Description 3"
    )
    information3 = Information.objects.create(
      text="Test Information 3", codex=codex3
    )

    response = self.client.get(self.url)

    self.assertEqual(len(response.data), 1)

    self.assertEqual(response.data[0]["id"], information3.id)
    self.assertEqual(response.data[0]["codex"], codex3.id)
    self.assertEqual(response.data[0]["text"], information3.text)
    self.assertEqual(
      response.data[0]["initial_hash"], java_string_hashcode(information3.text)
    )
    self.assertEqual(
      response.data[0]["creation_date"],
      information3.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data[0]["update_date"],
      information3.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

  def test_get_list_information_not_connected_return_401(self):
    """ Test if a un-connected user can list Information """
    self.client.logout()
    response = self.client.get(self.url)

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class InformationGetDetailViewTest(DefaultAPITestCase):
  def setUp(self):
    self.connect_default_user()
    self.codex = Codex.objects.create(
      title="Test Codex 1", author=self.default_user, description="Description 1"
    )
    self.information1 = Information.objects.create(
      text="Test Information 1", codex=self.codex
    )
    self.url = reverse("information-detail", args=[1])

  def test_get_detail_information_assert_return_http_200(self):
    """ Test if the view return a 200 Response """
    response = self.client.get(self.url)

    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_get_detail_information_assert_return_information(self):
    """ Test if the view return a unique of codex information """
    response = self.client.get(self.url)

    self.assertEqual(len(response.data), 6)

    self.assertEqual(response.data["id"], self.information1.id)
    self.assertEqual(response.data["codex"], self.codex.id)
    self.assertEqual(response.data["text"], self.information1.text)
    self.assertEqual(
      response.data["initial_hash"], java_string_hashcode(self.information1.text)
    )
    self.assertEqual(
      response.data["creation_date"],
      self.information1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertEqual(
      response.data["update_date"],
      self.information1.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

  def test_get_detail_information_not_exist_assert_return_http_404(self):
    """ Test if the view return a 404 Response if the codex information does not exist """
    response = self.client.get(reverse("information-detail", args=[2]))

    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_get_detail_information_of_other_user_assert_return_http_404(self):
    """ Test if the view return a 404 Response when trying to retrieve an other user codex information """
    self.connect_user("oz")
    response = self.client.get(self.url)

    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_codex_add_view_not_connected_return_401(self):
    """ Test if a un-connected user can retrieve a Codex information """
    self.client.logout()
    response = self.client.get(self.url)

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class InformationPostViewTest(DefaultAPITestCase):
  def setUp(self):
    self.connect_default_user()
    self.codex1 = Codex.objects.create(
      title="Test Codex 1", author=self.default_user, description="Description 1"
    )
    self.information1 = Information.objects.create(
      text="Test Information 1", codex=self.codex1
    )
    self.codex2 = Codex.objects.create(
      title="Test Codex 2", author=self.default_user, description="Description 2"
    )
    self.url = reverse("information-list")
    self.slug = "test-codex-2"
    self.data = {"codex": "2", "text": "Text 2"}

  def test_post_information_assert_return_http_201(self):
    """ Test if the view return a 201 Response """
    response = self.client.post(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  def test_post_information_text_missing_assert_return_http_400(self):
    """ Test if the view return a 400 Response if the text is missing """
    self.data.pop("text")
    response = self.client.post(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data["text"][0], "This field is required.")

  def test_post_information_title_missing_assert_return_http_400(self):
    """ Test if the view return a 400 Response if the codex id is missing """
    self.data.pop("codex")
    response = self.client.post(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data["codex"][0], "This field is required.")

  def test_post_information_codex_not_exist_assert_return_http_400(self):
    """ Test if the view return a 400 Response if the codex does not exist """
    self.data["codex"] = "3"
    response = self.client.post(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data["codex"][0], 'Invalid pk "3" - object does not exist.')

  def test_post_information_assert_create_information(self):
    """ Test if the information is created in the data base """
    self.client.post(self.url, self.data)
    information_list = Information.objects.all()
    new_information = Information.objects.filter(id=2)

    self.assertEqual(len(information_list), 2)
    self.assertEqual(len(new_information), 1)
    self.assertEqual(new_information[0].codex.id, int(self.data["codex"]))
    self.assertEqual(new_information[0].text, self.data["text"])

  def test_post_information_assert_return_information(self):
    """ Test if the view return an information """
    response = self.client.post(self.url, self.data)

    self.assertEqual(len(response.data), 6)

    self.assertEqual(response.data["id"], 2)
    self.assertEqual(response.data["codex"], self.codex2.id)
    self.assertEqual(response.data["text"], self.data["text"])
    self.assertEqual(
      response.data["initial_hash"], java_string_hashcode(self.data["text"])
    )
    self.assertIsNotNone(response.data["creation_date"])
    self.assertIsNotNone(response.data["update_date"])

  def test_post_information_assert_user_has_permissions(self):
    """ Test if the information is created with the correct permissions """
    self.client.post(self.url, self.data)
    information = Information.objects.get(id=2)

    self.assertEqual(self.default_user.has_perm('view_information', information), True)
    self.assertEqual(self.default_user.has_perm('change_information', information), True)
    self.assertEqual(self.default_user.has_perm('delete_information', information), True)

  def test_post_information_already_exist_assert_return_http_400(self):
    """ Test if the view return a 400 response if the information already exist """
    self.data["codex"] = "1"
    response = self.client.post(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(
      response.data["codex"][0], 'The specified Information already exist.'
    )

  def test_post_information_user_not_codex_owner_assert_return_http_400(self):
    """ Test if a user can create a information for aun-owned codex """
    self.connect_user("oz")
    response = self.client.post(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(
      response.data["codex"][0], 'Invalid pk "2" - object does not exist.'
    )

  def test_post_information_user_not_connected_assert_return_http_401(self):
    """ Test if a un-connected user can create a information """
    self.client.logout()
    response = self.client.post(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class InformationPutViewTest(DefaultAPITestCase):
  def setUp(self):
    self.connect_default_user()
    self.codex1 = Codex.objects.create(
      title="Test Codex 1", author=self.default_user, description="Description 1"
    )
    self.information1 = Information.objects.create(
      text="Test Information 1", codex=self.codex1
    )
    self.codex2 = Codex.objects.create(
      title="Test Codex 2", author=self.default_user, description="Description 2"
    )
    self.information2 = Information.objects.create(
      text="Test Information 2", codex=self.codex2
    )
    self.url = reverse("information-detail", args=[1])
    self.data = {
      "text": "Test Information 1 updated",
      "modification_hash": java_string_hashcode(self.information1.text),
    }

  def test_put_information_assert_return_http_200(self):
    """ Test if the view return a 200 Response """
    response = self.client.put(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_put_information_text_missing_assert_return_http_400(self):
    """ Test if the view return a 400 Response if the text is missing """
    self.data.pop("text")
    response = self.client.put(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data["text"][0], "This field is required.")

  def test_put_information_hash_missing_assert_return_http_400(self):
    """ Test if the view return a 400 Response if the hash is missing """
    self.data.pop("modification_hash")
    response = self.client.put(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(
      response.data["modification_hash"][0], "This field is required."
    )

  def test_put_information_hash_wrong_assert_return_http_400(self):
    """ Test if the view return a 400 Response if the hash is wrong """
    self.data["modification_hash"] = 0
    response = self.client.put(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(
      response.data["modification_hash"][0],
      "The Information have been modified since the last "
      "modification attempt.",
    )

  def test_put_information_assert_return_information(self):
    """ Test if the view return an information """
    response = self.client.put(self.url, self.data)

    self.assertEqual(len(response.data), 6)

    self.assertEqual(response.data["id"], self.information1.id)
    self.assertEqual(response.data["codex"], self.codex1.id)
    self.assertEqual(response.data["text"], self.data["text"])
    self.assertEqual(
      response.data["initial_hash"], java_string_hashcode(self.data["text"])
    )
    self.assertEqual(
      response.data["creation_date"],
      self.information1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    self.assertIsNotNone(response.data["update_date"])

  def test_put_information_assert_information_updated(self):
    """ Test if the information is updated in the data base """
    self.client.put(self.url, self.data)
    information_list = Information.objects.all()
    updated_information = Information.objects.filter(id=1)

    self.assertEqual(len(information_list), 2)
    self.assertEqual(len(updated_information), 1)
    self.assertEqual(updated_information[0].text, self.data["text"])

  def test_put_information_assert_other_information_not_updated(self):
    """ Test if other information are not updated in the data base """
    self.client.put(self.url, self.data)
    information2 = Information.objects.get(id=2)

    self.assertNotEqual(information2.text, self.data["text"])

  def test_put_information_not_exist_assert_return_http_404(self):
    """ Test if the view return a 404 Response if the information does not exist """
    response = self.client.put(reverse("information-detail", args=[3]), self.data)

    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_put_information_of_other_user_assert_return_http_404(self):
    """ Test if the view return a 404 Response when trying to update an other user codex """
    self.connect_user("oz")
    response = self.client.put(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_put_information_user_not_connected_return_401(self):
    """ Test if a un-connected user can update a Codex """
    self.client.logout()
    response = self.client.put(self.url, self.data)

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class InformationDeleteViewTest(DefaultAPITestCase):
  def setUp(self):
    self.connect_default_user()
    self.codex1 = Codex.objects.create(
      title="Test Codex 1", author=self.default_user, description="Description 1"
    )
    self.information1 = Information.objects.create(
      text="Test Information 1", codex=self.codex1
    )
    self.codex2 = Codex.objects.create(
      title="Test Codex 2", author=self.default_user, description="Description 2"
    )
    self.information2 = Information.objects.create(
      text="Test Information 2", codex=self.codex2
    )
    self.url = reverse("information-detail", args=[1])

  def test_delete_information_assert_return_http_204(self):
    """ Test if the view return a 204 Response """
    response = self.client.delete(self.url)

    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

  def test_delete_information_not_exist_assert_return_http_400(self):
    """ Test if the view return a 400 Response if the information does not exist """
    response = self.client.delete(reverse("information-detail", args=[3]))

    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_delete_information_assert_deleted_in_data_base(self):
    """ Test if the information is deleted in the data base """
    self.client.delete(self.url)
    information_list = Information.objects.all()
    new_information = Information.objects.filter(id=1)

    self.assertEqual(len(information_list), 1)

    self.assertEqual(len(new_information), 0)

  def test_delete_information_of_other_user_assert_return_http_404(self):
    """ Test if the view return a 404 Response when trying to delete an other user information """
    self.connect_user("oz")
    response = self.client.delete(self.url)

    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_delete_information_user_not_connected_assert_return_http_401(self):
    """ Test if a un-connected user can create an information """
    self.client.logout()
    response = self.client.delete(self.url)

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
