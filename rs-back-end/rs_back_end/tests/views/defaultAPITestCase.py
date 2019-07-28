from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class DefaultAPITestCase(APITestCase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.users = {}

  def create_user(self, username, email="default@email.com", password="top_secret"):
    self.users[username] = User.objects.create_user(
      username=username, email=email, password=password
    )
    Token.objects.get_or_create(user=self.users[username])
    # Add codex permissions
    assign_perm('rs_back_end.view_codex', self.users[username])
    assign_perm('rs_back_end.add_codex', self.users[username])
    assign_perm('rs_back_end.change_codex', self.users[username])
    assign_perm('rs_back_end.delete_codex', self.users[username])
    # Add information permissions
    assign_perm('rs_back_end.view_information', self.users[username])
    assign_perm('rs_back_end.add_information', self.users[username])
    assign_perm('rs_back_end.change_information', self.users[username])
    assign_perm('rs_back_end.delete_information', self.users[username])
    # Add page permissions
    assign_perm('rs_back_end.view_page', self.users[username])
    assign_perm('rs_back_end.add_page', self.users[username])
    assign_perm('rs_back_end.change_page', self.users[username])
    assign_perm('rs_back_end.delete_page', self.users[username])
    # Add task permissions
    assign_perm('rs_back_end.view_task', self.users[username])
    assign_perm('rs_back_end.add_task', self.users[username])
    assign_perm('rs_back_end.change_task', self.users[username])
    assign_perm('rs_back_end.delete_task', self.users[username])
    # Add note permissions
    assign_perm('rs_back_end.view_note', self.users[username])
    assign_perm('rs_back_end.add_note', self.users[username])
    assign_perm('rs_back_end.change_note', self.users[username])
    assign_perm('rs_back_end.delete_note', self.users[username])
    return self.users[username]

  def connect_user(self, username, email="default@email.com", password="top_secret"):
    user = self.users.get(username)
    if user is None:
      user = self.create_user(username=username, email=email, password=password)

    self.client.force_authenticate(user=user)

  def connect_default_user(self):
    self.connect_user(username="zamour")

  @property
  def default_user(self):
    return self.users["zamour"]
