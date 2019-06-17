from django.urls import reverse
from rest_framework import status

from projets.models import Codex
from projets.tests.views.defaultAPITestCase import DefaultAPITestCase


class CodexGetListViewTest(DefaultAPITestCase):
    def setUp(self):
        self.connect_default_user()
        self.codex1 = Codex.objects.create(
            title="Test Codex 1", author=self.default_user, description="Description 1"
        )
        self.codex2 = Codex.objects.create(
            title="Test Codex 2", author=self.default_user, description="Description 2"
        )
        self.url = reverse("codex-list")

    def test_get_list_codex_assert_return_http_200(self):
        """ Test if the view return a 200 Response """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_codex_assert_return_list(self):
        """ Test if the view return a list of codex """
        response = self.client.get(self.url)

        self.assertEqual(len(response.data), 2)

        self.assertEqual(response.data[0]['id'], self.codex1.id)
        self.assertEqual(response.data[0]['title'], self.codex1.title)
        self.assertEqual(response.data[0]['slug'], self.codex1.slug)
        self.assertEqual(response.data[0]['description'], self.codex1.description)
        self.assertEqual(response.data[0]['creation_date'], self.codex1.creation_date.strftime('%Y-%m-%dT%H:%M:%SZ'))
        self.assertEqual(response.data[0]['update_date'], self.codex1.update_date.strftime('%Y-%m-%dT%H:%M:%SZ'))
        self.assertEqual(response.data[0]['nested_update_date'],
                         self.codex1.nested_update_date.strftime('%Y-%m-%dT%H:%M:%SZ'))

        self.assertEqual(response.data[1]['id'], self.codex2.id)
        self.assertEqual(response.data[1]['title'], self.codex2.title)
        self.assertEqual(response.data[1]['slug'], self.codex2.slug)
        self.assertEqual(response.data[1]['description'], self.codex2.description)
        self.assertEqual(response.data[1]['creation_date'], self.codex2.creation_date.strftime('%Y-%m-%dT%H:%M:%SZ'))
        self.assertEqual(response.data[1]['update_date'], self.codex2.update_date.strftime('%Y-%m-%dT%H:%M:%SZ'))
        self.assertEqual(response.data[1]['nested_update_date'],
                         self.codex2.nested_update_date.strftime('%Y-%m-%dT%H:%M:%SZ'))

    def test_get_list_codex_return_only_self_codex(self):
        """ Test if a user can list Codex of other user """
        other_user_name = "oz"
        self.connect_user(username=other_user_name)
        codex3 = self.empty_codex = Codex.objects.create(
            title="Test Codex 3", author=self.users[other_user_name], description="Description 3"
        )

        response = self.client.get(self.url)

        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]['id'], codex3.id)
        self.assertEqual(response.data[0]['title'], codex3.title)
        self.assertEqual(response.data[0]['slug'], codex3.slug)
        self.assertEqual(response.data[0]['description'], codex3.description)
        self.assertEqual(response.data[0]['creation_date'], codex3.creation_date.strftime('%Y-%m-%dT%H:%M:%SZ'))
        self.assertEqual(response.data[0]['update_date'], codex3.update_date.strftime('%Y-%m-%dT%H:%M:%SZ'))
        self.assertEqual(response.data[0]['nested_update_date'],
                         codex3.nested_update_date.strftime('%Y-%m-%dT%H:%M:%SZ'))

    def test_get_list_codex_not_connected_return_401(self):
        """ Test if a un-connected user can list Codex """
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CodexGetDetailViewTest(DefaultAPITestCase):
    def setUp(self):
        self.connect_default_user()
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.default_user, description="Description 1"
        )
        self.empty_codex = Codex.objects.create(
            title="Test Codex 2", author=self.default_user, description="Description 2"
        )
        self.url = reverse("codex-detail", args=[self.codex.slug])

    def test_get_detail_codex_assert_return_http_200(self):
        """ Test if the view return a 200 Response """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_codex_assert_return_codex(self):
        """ Test if the view return a unique of codex """
        response = self.client.get(self.url)

        self.assertEqual(len(response.data), 7)

        self.assertEqual(response.data['id'], self.codex.id)
        self.assertEqual(response.data['title'], self.codex.title)
        self.assertEqual(response.data['slug'], self.codex.slug)
        self.assertEqual(response.data['description'], self.codex.description)
        self.assertEqual(response.data['creation_date'], self.codex.creation_date.strftime('%Y-%m-%dT%H:%M:%SZ'))
        self.assertEqual(response.data['update_date'], self.codex.update_date.strftime('%Y-%m-%dT%H:%M:%SZ'))
        self.assertEqual(response.data['nested_update_date'],
                         self.codex.nested_update_date.strftime('%Y-%m-%dT%H:%M:%SZ'))

    def test_get_detail_codex_not_exist_assert_return_http_400(self):
        """ Test if the view return a 400 Response if the codex does not exist """
        response = self.client.get(reverse("codex-detail", args=[3]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_detail_codex_of_other_user_assert_return_http_404(self):
        """ Test if the view return a 404 Response when trying to retrieve an other user codex """
        self.connect_user("oz")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_codex_add_view_not_connected_return_401(self):
        """ Test if a un-connected user can retrieve a Codex """
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CodexPostViewTest(DefaultAPITestCase):
    def setUp(self):
        self.connect_default_user()
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.default_user, description="Description 1"
        )
        self.slug = "test-codex-2"
        self.data = {"title": "Test Codex 2", "description": "Description 2"}
        self.url = reverse("codex-list")

    def test_post_codex_assert_return_http_201(self):
        """ Test if the view return a 201 Response """
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_codex_description_missing_assert_return_http_201(self):
        """ Test if the view return a 201 Response if the description is missing """
        data = {"title": "Test Codex 2"}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_codex_title_missing_assert_return_http_400(self):
        """ Test if the view return a 400 Response if the title is missing """
        data = {"description": "Description 2"}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['title'][0], 'This field is required.')

    def test_post_codex_assert_create_codex(self):
        """ Test if the codex is created in the data base """
        self.client.post(self.url, self.data)
        codex_list = Codex.objects.all()
        new_codex = Codex.objects.filter(id=2)

        self.assertEqual(len(codex_list), 2)
        self.assertEqual(len(new_codex), 1)
        self.assertEqual(new_codex[0].title, self.data["title"])
        self.assertEqual(new_codex[0].slug, self.slug)
        self.assertEqual(new_codex[0].description, self.data["description"])

    def test_post_codex_assert_return_codex(self):
        """ Test if the view return a codex """
        response = self.client.post(self.url, self.data)

        self.assertEqual(len(response.data), 7)

        self.assertEqual(response.data['id'], 2)
        self.assertEqual(response.data['title'], self.data["title"])
        self.assertEqual(response.data['slug'], self.slug)
        self.assertEqual(response.data['description'], self.data["description"])
        self.assertIsNotNone(response.data['creation_date'])
        self.assertIsNotNone(response.data['update_date'])
        self.assertIsNotNone(response.data['nested_update_date'])

    def test_post_codex_assert_user_has_permissions(self):
        """ Test if the codex is created with the correct permissions.py """
        self.client.post(self.url, self.data)
        codex = Codex.objects.get(id=2)

        self.assertEqual(self.default_user.has_perm('view_codex', codex), True)
        self.assertEqual(self.default_user.has_perm('change_codex', codex), True)
        self.assertEqual(self.default_user.has_perm('delete_codex', codex), True)

    def test_post_codex_user_not_connected_assert_return_http_401(self):
        """ Test if a un-connected user can create a Codex """
        self.client.logout()
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CodexPutViewTest(DefaultAPITestCase):
    def setUp(self):
        self.connect_default_user()
        self.codex1 = Codex.objects.create(
            title="Test Codex 1", author=self.default_user, description="Description 1"
        )
        self.codex2 = Codex.objects.create(
            title="Test Codex 2", author=self.default_user, description="Description 2"
        )
        self.data = {"title": "Test Codex 1 updated", "description": "Description 1 updated", }
        self.slug = "test-codex-1"
        self.url = reverse("codex-detail", args=[self.codex1.slug])

    def test_put_codex_assert_return_http_200(self):
        """ Test if the view return a 200 Response """
        response = self.client.put(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_codex_description_missing_assert_return_http_200(self):
        """ Test if the view return a 200 Response if the description is missing """
        data = {"title": "Test Codex 2"}
        response = self.client.put(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_codex_title_missing_assert_return_http_400(self):
        """ Test if the view return a 400 Response if the title is missing """
        data = {"description": "Description 2"}
        response = self.client.put(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['title'][0], 'This field is required.')

    def test_put_codex_assert_return_codex(self):
        """ Test if the view update a unique of codex """
        response = self.client.put(self.url, self.data)

        self.assertEqual(len(response.data), 7)

        self.assertEqual(response.data['id'], self.codex1.id)
        self.assertEqual(response.data['title'], self.data['title'])
        self.assertEqual(response.data['slug'], self.codex1.slug)
        self.assertEqual(response.data['description'], self.data['description'])
        self.assertEqual(response.data['creation_date'], self.codex1.creation_date.strftime('%Y-%m-%dT%H:%M:%SZ'))
        self.assertIsNotNone(response.data['update_date'])
        self.assertIsNotNone(response.data['nested_update_date'])

    def test_put_codex_assert_codex_updated(self):
        """ Test if the codex is updated in the data base """
        self.client.put(self.url, self.data)
        codex_list = Codex.objects.all()
        updated_codex = Codex.objects.filter(id=1)

        self.assertEqual(len(codex_list), 2)
        self.assertEqual(len(updated_codex), 1)
        self.assertEqual(updated_codex[0].title, self.data["title"])
        self.assertEqual(updated_codex[0].slug, self.slug)
        self.assertEqual(updated_codex[0].description, self.data["description"])

    def test_put_codex_assert_other_codex_not_updated(self):
        """ Test if other codex are not updated in the data base """
        self.client.put(self.url, self.data)
        codex2 = Codex.objects.get(id=2)

        self.assertNotEqual(codex2.title, self.data["title"])
        self.assertNotEqual(codex2.description, self.data["description"])

    def test_put_codex_not_exist_assert_return_http_400(self):
        """ Test if the view return a 400 Response if the codex does not exist """
        response = self.client.put(reverse("codex-detail", args=[3]), self.data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_codex_of_other_user_assert_return_http_404(self):
        """ Test if the view return a 404 Response when trying to update an other user codex """
        self.connect_user("oz")
        response = self.client.put(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_codex_not_connected_return_401(self):
        """ Test if a un-connected user can update a Codex """
        self.client.logout()
        response = self.client.put(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CodexDeleteViewTest(DefaultAPITestCase):
    def setUp(self):
        self.connect_default_user()
        self.codex1 = Codex.objects.create(
            title="Test Codex 1", author=self.default_user, description="Description 1"
        )
        self.codex2 = Codex.objects.create(
            title="Test Codex 2", author=self.default_user, description="Description 2"
        )
        self.url = reverse("codex-detail", args=[self.codex1.slug])

    def test_delete_codex_assert_return_http_201(self):
        """ Test if the view return a 204 Response """
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_codex_not_exist_assert_return_http_400(self):
        """ Test if the view return a 400 Response if the codex does not exist """
        response = self.client.delete(reverse("codex-detail", args=[3]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_codex_assert_create_codex(self):
        """ Test if the codex is deleted in the data base """
        self.client.delete(self.url)
        codex_list = Codex.objects.all()
        new_codex = Codex.objects.filter(id=1)

        self.assertEqual(len(codex_list), 1)

        self.assertEqual(len(new_codex), 0)

    def test_delete_codex_of_other_user_assert_return_http_404(self):
        """ Test if the view return a 404 Response when trying to delete an other user codex """
        self.connect_user("oz")

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_codex_user_not_connected_assert_return_http_401(self):
        """ Test if a un-connected user can create a Codex """
        self.client.logout()
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
