from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm

from projets.models import Codex, assign_all_perm, Task, Note, Information


def update_permissions():
    for user in (u for u in User.objects.all() if not u.is_anonymous):
        # Add codex permissions
        assign_perm('projets.view_codex', user)
        assign_perm('projets.add_codex', user)
        assign_perm('projets.change_codex', user)
        assign_perm('projets.delete_codex', user)
        # Add information permissions
        assign_perm('projets.view_information', user)
        assign_perm('projets.add_information', user)
        assign_perm('projets.change_information', user)
        assign_perm('projets.delete_information', user)
        # Add task permissions
        assign_perm('projets.view_task', user)
        assign_perm('projets.add_task', user)
        assign_perm('projets.change_task', user)
        assign_perm('projets.delete_task', user)
        # Add note permissions
        assign_perm('projets.view_note', user)
        assign_perm('projets.add_note', user)
        assign_perm('projets.change_note', user)
        assign_perm('projets.delete_note', user)

    for codex in (u for u in Codex.objects.all() if u.author and not u.author.is_anonymous):
        assign_all_perm(codex, codex.author)
        print("codex : " + str(codex))
        for information in Information.objects.filter(codex__author=codex.author):
            print("information : " + str(information))
            assign_all_perm(information, codex.author)
        for task in Task.objects.filter(page__codex__author=codex.author):
            print("task : " + str(task))
            assign_all_perm(task, codex.author)
        for note in Note.objects.filter(page__codex__author=codex.author):
            assign_all_perm(note, codex.author)
            print("note : " + str(note))
