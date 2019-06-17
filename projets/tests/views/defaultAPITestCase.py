from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm
from rest_framework.test import APITestCase


class DefaultAPITestCase(APITestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users = {}

    def create_user(self, username, email="default@email.com", password="top_secret"):
        self.users[username] = User.objects.create_user(
            username=username, email=email, password=password
        )
        # Add codex permissions
        assign_perm('projets.view_codex', self.users[username])
        assign_perm('projets.add_codex', self.users[username])
        assign_perm('projets.change_codex', self.users[username])
        assign_perm('projets.delete_codex', self.users[username])
        # Add information permissions
        assign_perm('projets.view_information', self.users[username])
        assign_perm('projets.add_information', self.users[username])
        assign_perm('projets.change_information', self.users[username])
        assign_perm('projets.delete_information', self.users[username])
        # Add task permissions
        assign_perm('projets.view_task', self.users[username])
        assign_perm('projets.add_task', self.users[username])
        assign_perm('projets.change_task', self.users[username])
        assign_perm('projets.delete_task', self.users[username])
        # Add note permissions
        assign_perm('projets.view_note', self.users[username])
        assign_perm('projets.add_note', self.users[username])
        assign_perm('projets.change_note', self.users[username])
        assign_perm('projets.delete_note', self.users[username])

    def connect_user(self, username, email="default@email.com", password="top_secret"):
        if self.users.get(username) is None:
            self.create_user(username=username, email=email, password=password)

        self.client.login(username=username, password=password)

    def connect_default_user(self):
        self.connect_user(username="zamour")

    @property
    def default_user(self):
        return self.users["zamour"]
