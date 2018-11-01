from django.forms import ModelForm, Textarea, HiddenInput, CheckboxInput, IntegerField

from .models import Projet, Main_Courante, Journal_Entree, TODO_Entree, Codex, Information, Note, Task


class CodexForm(ModelForm):
    class Meta:
        model = Codex
        fields = ('title', 'description')
        widgets = {
            'description': Textarea(attrs={'rows': 3, 'style': 'resize:none;'})
        }


class InformationForm(ModelForm):
    class Meta:
        model = Information
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={'rows': 3, 'style': 'resize:none;'})
        }


class NoteForm(ModelForm):
    note_id = IntegerField(widget=HiddenInput(attrs={'class': 'journal_entree_id'}), required=False)

    class Meta:
        model = Note
        fields = ('text',)
        widgets = {
            'text': Textarea(
                attrs={
                    'rows': 3,
                    'class': 'journal_entree_texte journal_typewatch',
                    'placeholder': 'Notes du jour',
                    'readonly': ''
                })
        }

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        # If an object is given as a parameter, the id field must be updated
        if self.instance:
            self.initial['note_id'] = self.instance.id

    def save(self, commit=True, page=None, *args, **kwargs):
        note = super(NoteForm, self).save(commit=False, *args, **kwargs)
        # Update the id as it cannot be retrieved by a ModelForm
        note.id = self.cleaned_data['note_id']
        # Set the note page that we get from the url
        note.page = page
        if commit:
            note.save()
        return note


class TaskForm(ModelForm):
    task_id = IntegerField(widget=HiddenInput(attrs={'class': 'todo_entree_id'}), required=False)

    class Meta:
        model = Task
        fields = ('text', 'is_achieved')
        widgets = {
            'text': Textarea(attrs={'rows': 1, 'class': 'todo_entree_texte', 'placeholder': 'Nouvelle tache'}),
            'is_achieved': CheckboxInput(attrs={'class': 'todo_entree_checkbox'})
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        # If an object is given as a parameter, the id field must be updated
        if self.instance:
            self.initial['task_id'] = self.instance.id

    def save(self, commit=True, page=None, *args, **kwargs):
        task = super(TaskForm, self).save(commit=False, *args, **kwargs)
        # Update the id as it cannot be retrieved by a ModelForm
        task.id = self.cleaned_data['task_id']
        # Set the task page that we get from the url
        task.page = page
        if commit:
            task.save()
        return task


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


class Journal_EntreeForm(ModelForm):
    
    journal_id = IntegerField(widget=HiddenInput(attrs={'class':'journal_entree_id'}), required=False)
    
    class Meta:
        model = Journal_Entree
        fields = ('texte',)
        widgets = {
            'texte': Textarea(attrs={'rows': 3,'class':'journal_entree_texte journal_typewatch','placeholder':'Notes du jour','readonly':''})
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
            'texte': Textarea(attrs={'rows': 1,'class':'todo_entree_texte','placeholder':'Nouvelle tache'}),
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