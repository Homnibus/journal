from django.contrib import admin
from .models import Projet, Main_Courante, Journal_Entree, TODO_Entree

admin.site.register(Projet)
admin.site.register(Main_Courante)
admin.site.register(Journal_Entree)
admin.site.register(TODO_Entree)
