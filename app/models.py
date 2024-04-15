# DJANGO DECLARATIONS
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count, F, Max, Min

# GENERAL DECLARATIONS
import os
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# DECLARING GLOBAL VARIABLES
SEXE_INTERLOCUTTEUR = [
    ('M.', 'M.'),
    ('Mme.', 'Mme.'),
]


STATUT_CYCLE = [
    ('En cours', 'En cours'),
    ('Payé', 'Payé'),
    ('Achevé', 'Achevé'),
]



class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_profile')
    complete_name = models.CharField(
        max_length=200,
        blank=False,
        null=False)
    permissions = models.TextField(default='*')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.complete_name
    

class Contrat(models.Model):
    numero_client = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default='')
    raison_sociale = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default='')
    rue = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        default='')
    zipcode = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default='')
    npa = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default='')
    localite = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        default='')
    sexe_interlocuteur = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=SEXE_INTERLOCUTTEUR,
        default='')
    nom_interlocuteur = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default='')
    prenom_interlocuteur = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default='')
    duree_contrat = models.IntegerField(default=0)
    date_contrat = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Declaration des fonctions de classe
    def is_termine(self):
        if Cycle.objects.filter(contrat=self, statut='Achevé').exists():
            return True
        
        return False
    
    def articles(self):
        return Article.objects.filter(contrat=self)

    def cycles(self):
        return Cycle.objects.filter(contrat=self).order_by("-id")
    
    def nb_cycles(self):
        return len(self.cycles())
    
    def nb_renouvelements(self):
        return len(Cycle.objects.filter(contrat=self, statut='Payé'))

    def cycle_encours(self):
        if not self.is_termine():
            return Cycle.objects.filter(contrat=self, statut='En cours')[0]
        else:
            return None
        
    def jours_au_payment(self):
        if not self.is_termine():
            cycle_encours = self.cycle_encours()
            return (cycle_encours.date_fin - date.today()).days
        else:
            return 0
        
    def nb_articles(self):
        return len(Article.objects.filter(contrat=self))
    
    def total_mensualites(self):
        total = 0
        articles = Article.objects.filter(contrat=self)
        for a in articles:
            total += a.mensualite
        return total
    
    def montant_renouvelement(self):
        return self.total_mensualites() * self.duree_contrat


class Article(models.Model):
    contrat = models.ForeignKey(
        Contrat, on_delete=models.CASCADE, null=False, blank=False)
    numero_mobile = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default='')
    designation = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default='')
    mensualite = models.FloatField(default=0)


class Cycle(models.Model):
    contrat = models.ForeignKey(
        Contrat, on_delete=models.CASCADE, null=False, blank=False)
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default='En cours',
        choices=STATUT_CYCLE)
    paye_le = models.DateField(null=True, blank=True)
    duree_prolongation = models.IntegerField(default = 0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_file(self):
        file_name = ""
        for filename in os.listdir('media/documents/'):
            name, extension = os.path.splitext(filename)
            if name == str(self.id):
                file_name = name + extension

        return file_name

    def pourcentage_cycle(self):
        if self.statut == 'Payé':
            return 100
        else:
            days_completed = (date.today() - self.date_debut).days
            cycle_periode = (self.date_fin - self.date_debut).days
            if cycle_periode > 0:
                return (days_completed/cycle_periode) * 100
            else:
                return 0

class PermissionsUserProfile(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=False, blank=False)
    permission_name = models.CharField(
        max_length=200,
        blank=False,
        null=False)
    views = models.TextField(null=False, blank=False)

