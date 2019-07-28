from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm

from rs_back_end.models import Codex, assign_all_perm, Task, Note, Information, Page


def update_permissions():
  for user in (u for u in User.objects.all() if not u.is_anonymous):
    # Add codex permissions
    assign_perm('rs_back_end.view_codex', user)
    assign_perm('rs_back_end.add_codex', user)
    assign_perm('rs_back_end.change_codex', user)
    assign_perm('rs_back_end.delete_codex', user)
    # Add information permissions
    assign_perm('rs_back_end.view_information', user)
    assign_perm('rs_back_end.add_information', user)
    assign_perm('rs_back_end.change_information', user)
    assign_perm('rs_back_end.delete_information', user)
    # Add task permissions
    assign_perm('rs_back_end.view_task', user)
    assign_perm('rs_back_end.add_task', user)
    assign_perm('rs_back_end.change_task', user)
    assign_perm('rs_back_end.delete_task', user)
    # Add note permissions
    assign_perm('rs_back_end.view_note', user)
    assign_perm('rs_back_end.add_note', user)
    assign_perm('rs_back_end.change_note', user)
    assign_perm('rs_back_end.delete_note', user)

  for codex in (u for u in Codex.objects.all() if u.author and not u.author.is_anonymous):
    assign_all_perm(codex, codex.author)
    print("codex : " + str(codex))
    for page in Page.objects.filter(codex__author=codex.author):
      print("page : " + str(page))
      assign_all_perm(page, codex.author)
    for information in Information.objects.filter(codex__author=codex.author):
      print("information : " + str(information))
      assign_all_perm(information, codex.author)
    for task in Task.objects.filter(page__codex__author=codex.author):
      print("task : " + str(task))
      assign_all_perm(task, codex.author)
    for note in Note.objects.filter(page__codex__author=codex.author):
      assign_all_perm(note, codex.author)
      print("note : " + str(note))
