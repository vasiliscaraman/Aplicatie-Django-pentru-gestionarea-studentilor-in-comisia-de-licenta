from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, IncarcarePDF
from django import forms
from datetime import datetime


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("nume", "initiala_tatalui", "prenume", "username", "email", "numar_telefon", "rol")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("nume", "initiala_tatalui", "prenume", "username", "email", "numar_telefon", "rol")


class InscriereForm(forms.ModelForm):
    class Meta:
        model = IncarcarePDF
        fields = ("titlul_lucrarii", "descrierea_lucrarii", "eseu", "fisa_inscriere", "declaratie_autenticitate")
















