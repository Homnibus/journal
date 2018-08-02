from django.db import models, connection
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Projet(models.Model):
    """ Objet de base du journal qui relie l'ensemble des pages d'un journal """
    titre = models.CharField(max_length=80, blank=False)
    createur = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    date_creation = models.DateTimeField(
        editable=False,
        verbose_name='Date de creation'
    )
    date_update = models.DateTimeField(
        verbose_name='Date de mise a jour'
    )
    
    def save(self, *args, **kwargs):
        """ Surcharge de la fonction save pour generer automatiquement le slug et la date de realisation. """
        # Dans le cas ou on cree l'objet la premiere fois
        if self.id is None:
            #maj de la date de creation
            self.date_creation = get_current_timestamp()
            #gestion de l'unicité du slug
            max_length = Projet._meta.get_field('slug').max_length
            self.slug = slugify(self.titre)[:max_length]
            original_slug = self.slug
            # Identifiant du slug pour avoir l'unicité
            i = 0 
            while Projet.objects.filter(slug=self.slug).exists():
                i += 1
                # Truncate the original slug dynamically. Minus 1 for the hyphen.
                self.slug = '%s-%d' % (original_slug[:max_length - len(str(i)) - 1], i) 
        #Dans tout les cas on met a jour la date de maj
        self.date_update = get_current_timestamp()        
        super(Projet, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.titre)

        
class Main_Courante(models.Model):
    """ Objet qui permet d'inscrire les info général d'un projet """
    projet = models.OneToOneField(
        Projet,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    texte = models.TextField(blank=True)
    date_creation = models.DateTimeField(
        editable=False,
        verbose_name='Date de creation'
    )
    date_update = models.DateTimeField(
        verbose_name='Date de mise a jour'
    )

    def save(self, *args, **kwargs):
        """Surcharge de la fonction save pour generer automatiquement la date de realisation"""
        # Dans le cas ou l'objet n'exite pas on ajoute manuellement la date de creation
        if self.date_creation is None:
            self.date_creation = get_current_timestamp()
        #Dans tout les cas on met a jour la date de maj
        self.date_update = get_current_timestamp()
        #Et on met a jours la date de maj du projet
        self.projet.save();
        super(Main_Courante, self).save(*args, **kwargs)
    
    def __str__(self):
        return ('Main courante pour ' + str(self.projet.titre))


class Journal_Entree(models.Model):
    """ Objet qui permet d'inscrire les realisation du jour """
    projet =  models.ForeignKey(Projet, on_delete=models.CASCADE)
    texte = models.TextField(blank=True)
    date_creation = models.DateTimeField(
        editable=False,
        verbose_name='Date de creation'
    )
    date_update = models.DateTimeField(
        verbose_name='Date de mise a jour'
    )

    def save(self, *args, **kwargs):
        """Surcharge de la fonction save pour generer automatiquement la date de realisation"""
        # Dans le cas ou l'objet n'exite pas on ajoute manuellement la date de creation
        if self.id is None:
            self.date_creation = get_current_timestamp()
        #Dans tout les cas on met a jour la date de maj
        self.date_update = get_current_timestamp()
        #Et on met a jours la date de maj du projet
        self.projet.save();
        super(Journal_Entree, self).save(*args, **kwargs)
    
    def __str__(self):
        return ('Entree du ' + str(self.date_creation) + ' pour le projet ' + str(self.projet))
        
        
class TODO_Entree(models.Model):
    """ Objet qui permet d'inscrire les taches à réaliser """
    projet =  models.ForeignKey(Projet, on_delete=models.CASCADE)
    texte = models.TextField(blank=True)
    realisee = models.BooleanField(default=False)
    date_creation = models.DateTimeField(
        editable=False,
        verbose_name='Date de creation'
    )
    date_update = models.DateTimeField(
        verbose_name='Date de mise a jour'
    )
    date_realisee = models.DateTimeField(
        null=True,
        verbose_name='Date de realisation'
    )
    
    def __init__(self, *args, **kwargs):
        super(TODO_Entree, self).__init__(*args, **kwargs)
        self.initial_realisee = self.realisee
    
    def save(self, *args, **kwargs):
        """Surcharge de la fonction save pour generer automatiquement la date de realisation"""
        # Dans le cas ou l'objet n'exite pas on ajoute manuellement la date de creation
        if self.id is None:
            self.date_creation = get_current_timestamp()
        #Si il vient d'être realisé, on met a jour la date de realisation
        if self.realisee == True and self.initial_realisee == False:
            self.date_realisee = get_current_timestamp()
        #Dans tout les cas on met a jour la date de maj
        self.date_update = get_current_timestamp()
        #Et on met a jours la date de maj du projet
        self.projet.save();
        super(TODO_Entree, self).save(*args, **kwargs)

    def __str__(self):
        return ('Projet : ' + str(self.projet) + " TODO : " + str(self.texte))
        

def get_current_timestamp():
    """ Fonction qui récupère la base de la BDD pour n'avoir qu'une seul source de date qui n'est pas du tout optimisé ! """
    cursor = connection.cursor()
    sql = cursor.execute('select current_timestamp')
    result = cursor.fetchone()    
    return result[0]       