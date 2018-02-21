from django.contrib import admin
from .models import Projet,Contact_Liste,Main_Courante,Journal_Entree,TODO_Entree

admin.site.register(Projet)
admin.site.register(Contact_Liste)
admin.site.register(Main_Courante)
admin.site.register(Journal_Entree)
admin.site.register(TODO_Entree)
