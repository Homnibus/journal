from time import sleep
from datetime import date

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from .models import Projet, Main_Courante, Journal_Entree, TODO_Entree, get_current_timestamp
from .views.codex_details_view import get_today_page

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

        
class ModelJournal_EntreeTest(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='zamour', email='zamour@zamour.com', password='top_secret')
        self.codex = Projet.objects.create(titre='codex 1',createur=self.user,description='description 1')
        self.codex.save()
                 
class ModelTODO_EntreeTest(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='zamour', email='zamour@zamour.com', password='top_secret')
        self.codex = Projet.objects.create(titre='codex 1',createur=self.user,description='description 1')
        self.codex.save()
         
    def test_creation(self):
        """ Test la creation d'un model TODO_Entree """

# ---
# Test de la classe codex
# ---

class codexTest(TestCase):
    
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='zamour', email='zamour@zamour.com', password='top_secret')        
        self.client.login(username='zamour', password='top_secret')
        self.codex1 = Projet.objects.create(titre='codex 1',createur=self.user,description='description 1')
        self.codex1.save()
        self.codex2 = Projet.objects.create(titre='codex 2',createur=self.user,description='description 2')
        self.codex2.save()

    def test_get_today_page_existe(self):
        # Test de récupération d'une Page vierge si la page du jour existe
        nouvelle_page = Journal_Entree.objects.create(projet=self.projet1,texte='texte 1')
        nouvelle_page.save()
        aujourdhui = get_current_timestamp()
        page_du_jour = get_today_page(self.codex1, aujourdhui)
        
        self.assertEqual(page_du_jour,nouvelle_page)
        #Ajouter le test sur les taches
        
    def test_get_today_page_not_existe(self):
        # Test de récupération d'une Page vierge si la page du jour n'existe pas
        aujourdhui = date(9999, 12, 30)
        page_du_jour = get_today_page(self.codex2, aujourdhui)

        self.assertEqual(page_du_jour.date,aujourdhui)
        self.assertIsNone(page_du_jour.texte)
    
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
    
    def test_get_today_page_not_existe(self):
        # Test de récupération d'une Page vierge si la page du jour n'existe pas
        today = date(9999, 12, 30)
        page_du_jour = get_today_page(self.codex1, today)
        self.assertEqual(page_du_jour.date,today)
        print(page_du_jour.journal_entry)
        #self.assertIsNone(page_du_jour.journal_entry.texte)
    
    
    
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