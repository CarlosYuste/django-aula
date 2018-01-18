# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Aula(models.Model):
    nom_aula = models.CharField(max_length=45, blank=True)
    descripcio_aula = models.CharField(max_length=240, blank=True, help_text="Exemple: Aforament màxim 30 persones. Exemple: 20 ordenadors sobretaula")
    disponibilitat_horaria = models.ManyToManyField('horaris.FranjaHoraria')
    horari_lliure = models.BooleanField(default=False)
    reservable = models.BooleanField(default=True)

    class Meta:
        ordering = ['nom_aula']
        verbose_name = 'Aula'
        verbose_name_plural = 'Aules'
    def __unicode__(self):
        return self.nom_aula if self.nom_aula + (self.descripcio_aula if self.descripcio_aula else '') else 'Sense nom'


class ReservaAula(models.Model):
    aula = models.ForeignKey(Aula, on_delete = models.PROTECT)
    dia_reserva = models.DateField()
    hora_inici = models.TimeField()
    hora_fi = models.TimeField()
    hora = models.ForeignKey('horaris.FranjaHoraria',null=True, blank=True)
    impartir = models.ForeignKey('presencia.Impartir', null=True, blank=True)
    usuari = models.ForeignKey(User)
    motiu = models.CharField(max_length=120, blank=False, help_text="No entrar dades personals, no entrar noms d'alumnes, no entrar noms de famílies")

    class Meta:
        ordering = ['dia_reserva', 'hora_inici']
        unique_together = [('aula', 'dia_reserva', 'hora_inici')]
    def __unicode__(self):
        return "{aula} {hora_inici}-{hora_fi} {usuari}".format(aula=self.aula, hora_inici=self.hora_inici, hora_fi=self.hora_fi, usuari = self.usuari)
