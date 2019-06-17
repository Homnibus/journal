from django.urls import reverse
from rest_framework import status

from projets.commun.utils import java_string_hashcode
from projets.models import Codex, Page, Task
from projets.tests.views.defaultAPITestCase import DefaultAPITestCase


class TaskGetListViewTest(DefaultAPITestCase):
    def setUp(self):
        self.connect_default_user()
        self.codex1 = Codex.objects.create(
            title="Test Codex 1", author=self.default_user, description="Description 1"
        )
        self.page1 = Page.objects.create(codex=self.codex1)
        self.task1 = Task.objects.create(page=self.page1, text="Test Task 1", is_achieved=True)
        self.codex2 = Codex.objects.create(
            title="Test Codex 2", author=self.default_user, description="Description 2"
        )
        self.page2 = Page.objects.create(codex=self.codex2)
        self.task2 = Task.objects.create(page=self.page2, text="Test Task 2")
        self.task3 = Task.objects.create(page=self.page2, text="Test Task 3")
        self.url = reverse("task-list")

    def test_get_list_task_assert_return_http_200(self):
        """ Test if the view return a 200 Response """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_task_assert_return_list(self):
        """ Test if the view return a list of task """
        response = self.client.get(self.url)

        self.assertEqual(len(response.data), 3)

        self.assertEqual(response.data[0]["id"], self.task1.id)
        self.assertEqual(response.data[0]["page"], self.page1.id)
        self.assertEqual(response.data[0]["text"], self.task1.text)
        self.assertEqual(response.data[0]["is_achieved"], self.task1.is_achieved)
        self.assertEqual(
            response.data[0]["initial_hash"],
            java_string_hashcode(self.task1.text),
        )
        self.assertEqual(
            response.data[0]["achieved_date"],
            self.task1.achieved_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        self.assertEqual(
            response.data[0]["creation_date"],
            self.task1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        self.assertEqual(
            response.data[0]["update_date"],
            self.task1.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )

        self.assertEqual(response.data[1]["id"], self.task2.id)
        self.assertEqual(response.data[1]["page"], self.page2.id)
        self.assertEqual(response.data[1]["text"], self.task2.text)
        self.assertEqual(response.data[1]["is_achieved"], self.task2.is_achieved)
        self.assertEqual(
            response.data[1]["initial_hash"],
            java_string_hashcode(self.task2.text),
        )
        self.assertIsNone(response.data[1]["achieved_date"])
        self.assertEqual(
            response.data[1]["creation_date"],
            self.task2.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        self.assertEqual(
            response.data[1]["update_date"],
            self.task2.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )

        self.assertEqual(response.data[2]["id"], self.task3.id)
        self.assertEqual(response.data[2]["page"], self.page2.id)
        self.assertEqual(response.data[2]["text"], self.task3.text)
        self.assertEqual(response.data[2]["is_achieved"], self.task3.is_achieved)
        self.assertEqual(
            response.data[2]["initial_hash"],
            java_string_hashcode(self.task3.text),
        )
        self.assertIsNone(response.data[2]["achieved_date"])
        self.assertEqual(
            response.data[2]["creation_date"],
            self.task3.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        self.assertEqual(
            response.data[2]["update_date"],
            self.task3.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )

    def test_get_filtered_list_task_assert_return_list(self):
        """ Test if the view return a list of filtered task """
        response = self.client.get(self.url + "?page__codex__slug=" + self.codex1.slug)

        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]["id"], self.task1.id)
        self.assertEqual(response.data[0]["page"], self.page1.id)
        self.assertEqual(response.data[0]["text"], self.task1.text)
        self.assertEqual(response.data[0]["is_achieved"], self.task1.is_achieved)
        self.assertEqual(
            response.data[0]["initial_hash"],
            java_string_hashcode(self.task1.text),
        )
        self.assertEqual(
            response.data[0]["achieved_date"],
            self.task1.achieved_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        self.assertEqual(
            response.data[0]["creation_date"],
            self.task1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        self.assertEqual(
            response.data[0]["update_date"],
            self.task1.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )

    def test_get_list_task_not_codex_author_return_only_self_codex(self):
        """ Test if a user can list task of other user """
        other_user_name = "oz"
        self.connect_user(other_user_name)
        codex3 = Codex.objects.create(
            title="Test Codex 3", author=self.users[other_user_name], description="Description 3"
        )
        page3 = Page.objects.create(codex=codex3)
        task4 = Task.objects.create(page=page3, text="Test Task 4")

        response = self.client.get(self.url)

        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]["id"], task4.id)
        self.assertEqual(response.data[0]["page"], page3.id)
        self.assertEqual(response.data[0]["text"], task4.text)
        self.assertEqual(response.data[0]["is_achieved"], task4.is_achieved)
        self.assertEqual(
            response.data[0]["initial_hash"],
            java_string_hashcode(task4.text),
        )
        self.assertIsNone(response.data[0]["achieved_date"])
        self.assertEqual(
            response.data[0]["creation_date"],
            task4.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        self.assertEqual(
            response.data[0]["update_date"],
            task4.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )

    def test_get_list_task_not_connected_return_401(self):
        """ Test if a un-connected user can list task """
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TaskGetDetailViewTest(DefaultAPITestCase):
    def setUp(self):
        self.connect_default_user()
        self.codex = Codex.objects.create(
            title="Test Codex 1", author=self.default_user, description="Description 1"
        )
        self.page = Page.objects.create(codex=self.codex)
        self.task = Task.objects.create(page=self.page, text="Test Task 1")
        self.url = reverse("task-detail", args=[1])

    def test_get_detail_task_assert_return_http_200(self):
        """ Test if the view return a 200 Response """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_task_assert_return_task(self):
        """ Test if the view return a unique task """
        response = self.client.get(self.url)

        self.assertEqual(len(response.data), 8)

        self.assertEqual(response.data["id"], self.task.id)
        self.assertEqual(response.data["page"], self.page.id)
        self.assertEqual(response.data["text"], self.task.text)
        self.assertEqual(response.data["is_achieved"], self.task.is_achieved)
        self.assertEqual(
            response.data["initial_hash"],
            java_string_hashcode(self.task.text),
        )
        self.assertIsNone(response.data["achieved_date"])
        self.assertEqual(
            response.data["creation_date"],
            self.task.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        self.assertEqual(
            response.data["update_date"],
            self.task.update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )

    def test_get_detail_task_not_exist_assert_return_http_404(self):
        """ Test if the view return a 404 Response if the task does not exist """
        response = self.client.get(reverse("task-detail", args=[2]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_detail_task_of_other_user_assert_return_http_404(self):
        """ Test if the view return a 404 Response when trying to retrieve an other user task """
        self.connect_user("oz")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_detail_task_user_not_connected_return_401(self):
        """ Test if a un-connected user can retrieve a task """
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TaskPostViewTest(DefaultAPITestCase):
    def setUp(self):
        self.connect_default_user()
        self.codex1 = Codex.objects.create(
            title="Test Codex 1", author=self.default_user, description="Description 1"
        )
        self.page1 = Page.objects.create(codex=self.codex1)
        self.task1 = Task.objects.create(page=self.page1, text="Test Task 1")
        self.codex2 = Codex.objects.create(
            title="Test Codex 2", author=self.default_user, description="Description 2"
        )
        self.url = reverse("task-list")
        self.slug = "test-codex-2"
        self.data = {"codex": "2", "text": "Text 2", "is_achieved": "True"}

    def test_post_task_assert_return_http_201(self):
        """ Test if the view return a 201 Response """
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_task_text_missing_assert_return_http_400(self):
        """ Test if the view return a 400 Response if the text is missing """
        self.data.pop("text")
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["text"][0], "This field is required.")

    def test_post_task_codex_missing_assert_return_http_400(self):
        """ Test if the view return a 400 Response if the codex id is missing """
        self.data.pop("codex")
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["codex"][0], "This field is required.")

    def test_post_task_is_achieved_missing_assert_return_http_201(self):
        """ Test if the view return a 201 Response if the is achieved boolean is missing """
        self.data.pop("is_achieved")
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_task_codex_not_exist_assert_return_http_400(self):
        """ Test if the view return a 400 Response if the codex does not exist """
        self.data["codex"] = "3"
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["codex"][0], "The specified Codex does not exist.")

    def test_post_task_assert_create_task(self):
        """ Test if the task is created in the data base """
        self.client.post(self.url, self.data)
        task_list = Task.objects.all()
        new_task = Task.objects.filter(id=2)

        self.assertEqual(len(task_list), 2)
        self.assertEqual(len(new_task), 1)
        self.assertEqual(new_task[0].page.codex.id, int(self.data["codex"]))
        self.assertEqual(new_task[0].text, self.data["text"])
        self.assertEqual(str(new_task[0].is_achieved), self.data["is_achieved"])

    def test_post_task_assert_return_task(self):
        """ Test if the view return a task """
        response = self.client.post(self.url, self.data)

        self.assertEqual(len(response.data), 8)

        self.assertEqual(response.data["id"], 2)
        self.assertEqual(response.data["page"], 2)
        self.assertEqual(response.data["text"], self.data["text"])
        self.assertEqual(str(response.data["is_achieved"]), self.data["is_achieved"])
        self.assertEqual(
            response.data["initial_hash"],
            java_string_hashcode(self.data["text"]),
        )
        self.assertIsNotNone(response.data["achieved_date"])
        self.assertIsNotNone(response.data["creation_date"])
        self.assertIsNotNone(response.data["update_date"], )

    def test_post_task_assert_user_has_permissions(self):
        """ Test if the task is created with the correct permissions.py """
        self.client.post(self.url, self.data)
        task = Task.objects.get(id=2)

        self.assertEqual(self.default_user.has_perm('view_task', task), True)
        self.assertEqual(self.default_user.has_perm('change_task', task), True)
        self.assertEqual(self.default_user.has_perm('delete_task', task), True)

    def test_post_task_already_exist_assert_return_http_201(self):
        """ Test if the view return a 201 response if a task already exist for the given codex """
        self.data["codex"] = "1"
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_task_user_not_codex_owner_assert_return_http_403(self):
        """ Test if a user can create a task for a un-owned codex """
        self.connect_user("oz")
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_task_user_not_connected_assert_return_http_401(self):
        """ Test if a un-connected user can create a Task """
        self.client.logout()
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TaskPutViewTest(DefaultAPITestCase):
    def setUp(self):
        self.connect_default_user()
        self.codex1 = Codex.objects.create(
            title="Test Codex 1", author=self.default_user, description="Description 1"
        )
        self.page1 = Page.objects.create(codex=self.codex1)
        self.task1 = Task.objects.create(text="Test task 1", page=self.page1)
        self.codex2 = Codex.objects.create(
            title="Test Codex 2", author=self.default_user, description="Description 2"
        )
        self.page2 = Page.objects.create(codex=self.codex2)
        self.task2 = Task.objects.create(text="Test task 2", page=self.page2)
        self.url = reverse("task-detail", args=[1])
        self.data = {
            "text": "Test task 1 updated",
            "is_achieved": "True",
            "modification_hash": java_string_hashcode(self.task1.text),
        }

    def test_put_task_assert_return_http_200(self):
        """ Test if the view return a 200 Response """
        response = self.client.put(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_task_text_missing_assert_return_http_400(self):
        """ Test if the view return a 400 Response if the text is missing """
        self.data.pop("text")
        response = self.client.put(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["text"][0], "This field is required.")

    def test_put_task_hash_missing_assert_return_http_400(self):
        """ Test if the view return a 400 Response if the hash is missing """
        self.data.pop("modification_hash")
        response = self.client.put(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["modification_hash"][0], "This field is required."
        )

    def test_put_task_is_achieved_missing_assert_return_http_200(self):
        """ Test if the view return a 200 Response if the is achieved boolean is missing """
        self.data.pop("is_achieved")
        response = self.client.put(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_task_hash_wrong_assert_return_http_400(self):
        """ Test if the view return a 400 Response if the hash is wrong """
        self.data["modification_hash"] = 0
        response = self.client.put(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["modification_hash"][0],
            "The Task have been modified since the last "
            "modification attempt.",
        )

    def test_put_task_assert_return_task(self):
        """ Test if the view return an task """
        response = self.client.put(self.url, self.data)

        self.assertEqual(len(response.data), 8)

        self.assertEqual(response.data["id"], self.task1.id)
        self.assertEqual(response.data["page"], self.page1.id)
        self.assertEqual(response.data["text"], self.data["text"])
        self.assertEqual(str(response.data["is_achieved"]), self.data["is_achieved"])
        self.assertEqual(response.data["initial_hash"], java_string_hashcode(self.data["text"]))
        self.assertIsNotNone(response.data["achieved_date"])
        self.assertEqual(
            response.data["creation_date"],
            self.task1.creation_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        )
        self.assertIsNotNone(response.data["update_date"])

    def test_put_task_assert_task_updated(self):
        """ Test if the task is updated in the data base """
        self.client.put(self.url, self.data)
        task_list = Task.objects.all()
        updated_task = Task.objects.filter(id=1)

        self.assertEqual(len(task_list), 2)
        self.assertEqual(len(updated_task), 1)
        self.assertEqual(updated_task[0].text, self.data["text"])

    def test_put_task_assert_other_task_not_updated(self):
        """ Test if other task are not updated in the data base """
        self.client.put(self.url, self.data)
        task2 = Task.objects.get(id=2)

        self.assertNotEqual(task2.text, self.data["text"])

    def test_put_task_not_exist_assert_return_http_404(self):
        """ Test if the view return a 404 Response if the task does not exist """
        response = self.client.put(reverse("task-detail", args=[3]), self.data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_task_of_other_user_assert_return_http_404(self):
        """ Test if the view return a 404 Response when trying to update an other user codex """
        self.connect_user("oz")
        response = self.client.put(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_codex_not_connected_return_401(self):
        """ Test if a un-connected user can update a Codex """
        self.client.logout()
        response = self.client.put(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TaskDeleteViewTest(DefaultAPITestCase):
    def setUp(self):
        self.connect_default_user()
        self.codex1 = Codex.objects.create(
            title="Test Codex 1", author=self.default_user, description="Description 1"
        )
        self.page1 = Page.objects.create(codex=self.codex1)
        self.task1 = Task.objects.create(page=self.page1, text="Test Task 1")
        self.codex2 = Codex.objects.create(
            title="Test Codex 2", author=self.default_user, description="Description 2"
        )
        self.page2 = Page.objects.create(codex=self.codex2)
        self.task2 = Task.objects.create(page=self.page2, text="Test Task 2")
        self.url = reverse("task-detail", args=[1])

    def test_delete_task_assert_return_http_204(self):
        """ Test if the view return a 204 Response """
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_task_not_exist_assert_return_http_400(self):
        """ Test if the view return a 400 Response if the task does not exist """
        response = self.client.delete(reverse("task-detail", args=[3]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_task_assert_task_deleted(self):
        """ Test if the task is deleted in the data base """
        self.client.delete(self.url)
        task_list = Task.objects.all()
        new_task = Task.objects.filter(id=1)

        self.assertEqual(len(task_list), 1)

        self.assertEqual(len(new_task), 0)

    def test_delete_task_of_other_user_assert_return_http_404(self):
        """ Test if the view return a 404 Response when trying to delete an other user task """
        self.connect_user("oz")
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_task_user_not_connected_assert_return_http_401(self):
        """ Test if a un-connected user can create an task """
        self.client.logout()
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
