from django.forms import (Form, ModelForm, Textarea, BaseModelFormSet, CharField, PasswordInput, HiddenInput
    , CheckboxInput, IntegerField, CharField, BooleanField, Widget)
                          
from .models import Projet, Main_Courante, Contact_Liste, Journal_Entree, TODO_Entree


class ProjetForm(ModelForm):
    class Meta:
        model = Projet
        fields=('titre','description',)
        widgets = {
            'description': Textarea(attrs={'rows': 3,'style':'resize:none;'}),
        }

        
class Main_CouranteForm(ModelForm):
    class Meta:
        model = Main_Courante
        fields=('texte',)
        widgets = {
            'texte': Textarea(attrs={'rows': 3,'style':'resize:none;'}),
        }

        
class Contact_ListeForm(ModelForm):
    class Meta:
        model = Contact_Liste
        fields=('texte',)
        widgets = {
            'texte': Textarea(attrs={'rows': 3,'style':'resize:none;'}),
        }

        
class Journal_EntreeForm(ModelForm):
    
    journal_id = IntegerField(widget=HiddenInput(attrs={'class':'journal_entree_id'}), required=False)
    
    class Meta:
        model = Journal_Entree
        fields = ('texte',)
        widgets = {
            'texte': Textarea(attrs={'rows': 3,'style':'resize:none;','class':'journal_entree_texte journal_typewatch'})
        }

    def __init__(self, *args, **kwargs):
        super(Journal_EntreeForm, self).__init__(*args, **kwargs)
        #Si un objet est passé en argument, on doit mettre a jour notre champ id
        if self.instance:
            self.initial['journal_id'] = self.instance.id
     
    def save(self, commit=True,projet=None, *args, **kwargs):
        journal_model = super(Journal_EntreeForm, self).save(commit=False, *args, **kwargs)
        #Gestion de l'id qui n'est pas possible de retourné de base avec un modelForm
        journal_model.id = self.cleaned_data['journal_id']    
        #Gestion du projet qui est passé dans la query et non dans le form
        journal_model.projet=projet
        if commit:
            journal_model.save()
        return journal_model
        
class TODO_EntreeForm(ModelForm):

    todo_id = IntegerField(widget=HiddenInput(attrs={'class':'todo_entree_id'}), required=False)
    
    class Meta:
        model = TODO_Entree
        fields = ('texte','realisee')
        widgets = {
            'texte': Textarea(attrs={'rows': 1,'style':'resize:none;','class':'todo_entree_texte todo_typewatch'}),
            'realisee': CheckboxInput(attrs={'class':'todo_entree_checkbox'},)
        }
    
    def __init__(self, *args, **kwargs):
        super(TODO_EntreeForm, self).__init__(*args, **kwargs)
        #Si un objet est passé en argument, on doit mettre a jour notre champ id
        if self.instance:
            self.initial['todo_id'] = self.instance.id
     
    def save(self, commit=True,projet=None, *args, **kwargs):
        todo_model = super(TODO_EntreeForm, self).save(commit=False, *args, **kwargs)
        #Gestion de l'id qui n'est pas possible de retourné de base avec un modelForm
        todo_model.id = self.cleaned_data['todo_id']    
        #Gestion du projet qui est passé dans la query et non dans le form
        todo_model.projet=projet
        if commit:
            todo_model.save()
        return todo_model