from statistics import mean

from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


# Create your models here.


class CustomUser(AbstractUser):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')
    rejection_reason = models.TextField(blank=True, null=True)
    nota1 = models.JSONField(default=list, blank=True)  # Stocam nota1 si nota 2 ca liste de floats
    nota2 = models.JSONField(default=list, blank=True)
    notaFinala = models.FloatField(default=0.0, blank=True)  # va fi media dintre nota1 si nota2

    class Roluri(models.TextChoices):
        Student = 'Student'
        Secretar = 'Secretar'
        Membru_comisie = 'Membru comisie'

    email = models.EmailField()
    nume = models.CharField(max_length=30, blank=True, null=True)
    initiala_tatalui = models.CharField(max_length=1)
    prenume = models.CharField(max_length=50, blank=True, null=True)
    numar_telefon = models.CharField(max_length=100, blank=True, null=True)
    rol = models.CharField(max_length=20, choices=Roluri.choices, default=Roluri.Student)
    este_inscris = models.BooleanField(default=False)
    afisare_note = models.BooleanField(default=False)

    def is_role(self):
        return self.rol

    def inscris(self):
        return self.este_inscris

    def __str__(self):
        return self.username

    @property
    def notaFinalaCalcul(self):
        if self.nota1 and self.nota2:
            return round((mean(self.nota1) + mean(self.nota2)) / 2, 2)
        else:
            return None


class IncarcarePDF(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    titlul_lucrarii = models.CharField(max_length=100)
    descrierea_lucrarii = models.TextField(max_length=3000)
    nume_student = models.CharField(max_length=30)
    initiala_tatalui = models.CharField(max_length=1)
    prenume_student = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True, editable=False)
    eseu = models.FileField(upload_to='pdfs/', blank=True, null=True)
    fisa_inscriere = models.FileField(upload_to='registration_papers/', blank=True, null=True)
    declaratie_autenticitate = models.FileField(upload_to='declarations/', blank=True, null=True)

    def user_exists(self):
        return self.user

    def __str__(self):
        return self.titlul_lucrarii
