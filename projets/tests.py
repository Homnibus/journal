from time import sleep

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from .models import Projet, Main_Courante, Contact_Liste, Journal_Entree, TODO_Entree

# Create your tests here.

# ---
# Test des Models
# ---
class ModelProjetTest(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='zamour', email='zamour@zamour.com', password='top_secret')
        self.codex1 = Projet.objects.create(titre='codex 1',createur=self.user,description='description 1')
        self.codex1.save()
        self.codex1bis = Projet.objects.create(titre='codex 1',createur=self.user,description='description 2')
        self.codex1bis.save()

         
    def test_creation(self):
        """ Test la creation d'un model Projet """
        codex = self.codex1
        
        self.assertIsNotNone(codex)
        self.assertIsNotNone(codex.date_creation)
        self.assertIsNotNone(codex.date_update)
        self.assertGreaterEqual(codex.date_update, codex.date_creation)
        self.assertEqual(codex.titre,'codex 1')
        self.assertEqual(codex.slug,'codex-1')
        self.assertEqual(codex.description,'description 1')
        self.assertIs(codex.createur,self.user)        
        # with self.assertRaises(Exception):
            # Projet.objects.create(titre='')
        
        
    def test_creation_bis(self):
        """ Test la creation d'un codex avec un nom déjà pris model Projet """
        codex = self.codex1bis
        
        self.assertIsNotNone(codex)
        self.assertEqual(codex.titre,'codex 1')
        self.assertEqual(codex.slug,'codex-1-1')
    
    def test_maj(self):
        """ Test d'une mise à jour """
    
class ModelMain_CouranteTest(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='zamour', email='zamour@zamour.com', password='top_secret')
        self.codex = Projet.objects.create(titre='codex 1',createur=self.user,description='description 1')
        self.codex.save()
        self.info1 = Main_Courante.objects.create(projet=self.codex,texte='texte 1')
        self.info1.save()
         
    def test_creation(self):
        """ Test la creation d'un model Main_Courante """
        info = self.info1
        
        self.assertIsNotNone(info)
        self.assertIsNotNone(info.date_creation)
        self.assertIsNotNone(info.date_update)
        self.assertGreaterEqual(info.date_update, info.date_creation)
        self.assertIs(info.projet,self.codex)
        self.assertEqual(info.texte,'texte 1')
        with self.assertRaises(ObjectDoesNotExist):
            Main_Courante.objects.create(projet=None)
        
        
    def test_creation_bis(self):
        """ Test la creation d'un deuxième model Main_Courante pour un projet donné """
        
        with self.assertRaises(IntegrityError):
            Main_Courante.objects.create(projet=self.codex)

    def test_maj(self):
        """ Test d'une mise à jour """

class ModelContact_ListeTest(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='zamour', email='zamour@zamour.com', password='top_secret')
        self.codex = Projet.objects.create(titre='codex 1',createur=self.user,description='description 1')
        self.codex.save()
        self.contact1 = Contact_Liste.objects.create(projet=self.codex,texte='texte 1')
        self.contact1.save()
         
    def test_creation(self):
        """ Test la creation d'un model Contact_Liste """
        contact = self.contact1
        
        self.assertIsNotNone(contact)
        self.assertIsNotNone(contact.date_creation)
        self.assertIsNotNone(contact.date_update)
        self.assertGreaterEqual(contact.date_update, contact.date_creation)
        self.assertIs(contact.projet,self.codex)
        self.assertEqual(contact.texte,'texte 1')
        with self.assertRaises(ObjectDoesNotExist):
            Contact_Liste.objects.create(projet=None)
        
        
    def test_creation_bis(self):
        """ Test la creation d'un deuxième model Contact_Liste pour un projet donné """
        
        with self.assertRaises(IntegrityError):
            Contact_Liste.objects.create(projet=self.codex)

    def test_maj(self):
        """ Test d'une mise à jour """

class ModelJournal_EntreeTest(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='zamour', email='zamour@zamour.com', password='top_secret')
        self.codex = Projet.objects.create(titre='codex 1',createur=self.user,description='description 1')
        self.codex.save()
        self.contact1 = Journal_Entree.objects.create(projet=self.codex,texte='texte 1')
        self.contact1.save()
         
    def test_creation(self):
        """ Test la creation d'un model Journal_Entree """
        contact = self.contact1
        
        self.assertIsNotNone(contact)
        self.assertIsNotNone(contact.date_creation)
        self.assertIsNotNone(contact.date_update)
        self.assertGreaterEqual(contact.date_update, contact.date_creation)
        self.assertIs(contact.projet,self.codex)
        self.assertEqual(contact.texte,'texte 1')
        with self.assertRaises(ObjectDoesNotExist):
            Journal_Entree.objects.create(projet=None)
        
    def test_maj(self):
        """ Test d'une mise à jour """
        
class ModelTODO_EntreeTest(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='zamour', email='zamour@zamour.com', password='top_secret')
        self.codex = Projet.objects.create(titre='codex 1',createur=self.user,description='description 1')
        self.codex.save()
        self.contact1 = TODO_Entree.objects.create(projet=self.codex,texte='texte 1')
        self.contact1.save()
         
    def test_creation(self):
        """ Test la creation d'un model TODO_Entree """
        contact = self.contact1
        
        self.assertIsNotNone(contact)
        self.assertIsNotNone(contact.date_creation)
        self.assertIsNotNone(contact.date_update)
        self.assertGreaterEqual(contact.date_update, contact.date_creation)
        self.assertIs(contact.projet,self.codex)
        self.assertEqual(contact.texte,'texte 1')
        with self.assertRaises(ObjectDoesNotExist):
            TODO_Entree.objects.create(projet=None)
        
    def test_maj(self):
        """ Test d'une mise à jour """
        
        
# ---
# Test des vues
# ---
class Viewcreer_codexTest(TestCase):
    
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='zamour', email='zamour@zamour.com', password='top_secret')        
        self.client.login(username='zamour', password='top_secret')
    
    def test_get(self):
        # Test de chargement de la page
        reponse = self.client.get(reverse('nouveau_codex'))
        self.assertEqual(reponse.status_code, 200)
        
    def test_post(self):
        # Test de creation d'un nouveau Codex
        data = {
            'titre':"titre c",
            'description':"description c",
        }
        
        reponse = self.client.post(reverse('nouveau_codex'), data, follow=True)
        codex_liste = Projet.objects.all()

        self.assertEqual(reponse.status_code, 200)
        self.assertIsNotNone(codex_liste)
        self.assertEqual(len(codex_liste), 1)
        self.assertEqual(codex_liste[0].titre, 'titre c')
        self.assertEqual(codex_liste[0].slug, 'titre-c')
        self.assertEqual(codex_liste[0].description, 'description c')

    
    def test_securite(self):
        # Test de creation d'un Codex sans être connecté
        data = {
            'titre':"titre c",
            'description':"description c",
        }        
        self.client.logout()
        
        reponse = self.client.post(reverse('nouveau_codex'), data)
        codex_liste = Projet.objects.all()
        
        self.assertEqual(len(codex_liste), 0)
        self.assertRedirects(reponse, reverse('connexion')+"?next="+reverse('nouveau_codex'), status_code=302, target_status_code=200)
        
        
class Viewafficher_codexTest(TestCase):
    
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='zamour', email='zamour@zamour.com', password='top_secret')        
        self.client.login(username='zamour', password='top_secret')
        self.codex1 = Projet.objects.create(titre='codex 1',createur=self.user,description='description 1')
        self.codex1.save()
    
    def test_get_existe(self):
        # Test d'affichage d'un codex qui existe
        reponse = self.client.get(reverse('afficher_codex',kwargs={'slug': 'codex-1'}))
        self.assertEqual(reponse.status_code, 200)

    def test_get_not_existe(self):
        # Test d'affichage d'un codex qui n'existe pas
        reponse = self.client.get(reverse('afficher_codex',kwargs={'slug': 'codex 1'}))
        self.assertEqual(reponse.status_code, 404)
        
    def test_securite(self):
        # Test de récupération d'un codex sans être connecté
        self.client.logout()
        
        reponse = self.client.get(reverse('afficher_codex',kwargs={'slug': 'codex-1'}))
        
        self.assertRedirects(reponse, reverse('connexion')+"?next="+reverse('afficher_codex',kwargs={'slug': 'codex-1'}), status_code=302, target_status_code=200)