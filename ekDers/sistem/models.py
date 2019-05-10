from django.db import models
from django.contrib.auth.models import User
from .choices import BOLUM_CHOICES
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bolum = models.CharField(max_length=30, choices=BOLUM_CHOICES, verbose_name='Bolumu')
    fakulte = models.CharField(max_length=30, verbose_name='Fakultesi')
    dersYuku = models.PositiveSmallIntegerField(verbose_name='dersYuku', default=10)

    def isim(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class BolumBaskani(models.Model):
    ad = models.CharField(max_length=50, verbose_name = 'Adı')
    bolum = models.CharField(max_length=50, verbose_name = 'Bolum')

    def __str__(self):
        return f'{self.ad} {self.bolum}'


class Dersler(models.Model):
    dersKodu = models.CharField(max_length=30, verbose_name='Ders Kodu')
    dersAdı = models.CharField(max_length=100, verbose_name='Ders Adı')
    dersiVeren = models.CharField(max_length=50, verbose_name='Dersi Veren')
    dersKredisi = models.CharField(max_length=15, verbose_name='Ders Kredisi')
    ikinciOgretim = models.BooleanField(default=False, verbose_name='İkinci Öğretim')
    def get_update_url(self):
        return reverse('sistem:update', kwargs={'id':self.id})

    def get_delete_url(self):
        return reverse('sistem:delete', kwargs={'id':self.id})

