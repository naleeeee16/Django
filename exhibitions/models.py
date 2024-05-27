# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from nft.models import Nft
from profiles.models import Registrovanikorisnik


class Izlozba(models.Model):
    idlis = models.OneToOneField('Listanft', models.CASCADE, db_column='IdLis', primary_key=True)  # Field name made lowercase.
    naziv = models.CharField(db_column='Naziv', max_length=18, blank=True, null=True)  # Field name made lowercase.
    opis = models.CharField(db_column='Opis', max_length=128, blank=True, null=True)  # Field name made lowercase.
    datumkreiranja = models.CharField(db_column='DatumKreiranja', max_length=18, blank=True, null=True)  # Field name made lowercase.
    prosecnaocena = models.CharField(db_column='ProsecnaOcena', max_length=18, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'izlozba'
        app_label = 'exhibitions'



class Kolekcija(models.Model):
    idlis = models.OneToOneField('Listanft', models.CASCADE, db_column='IdLis', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'kolekcija'
        app_label = 'exhibitions'



class Listanft(models.Model):
    idlis = models.AutoField(db_column='IdLis', primary_key=True)  # Field name made lowercase.
    idvla = models.ForeignKey(Registrovanikorisnik, models.CASCADE, db_column='IdVla', null=True)  # Field name made lowercase.
    ukupnavrednost = models.FloatField(db_column='UkupnaVrednost')  # Field name made lowercase.
    brojnft = models.IntegerField(db_column='BrojNFT')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'listanft'
        app_label = 'exhibitions'



class Portfolio(models.Model):
    idlis = models.OneToOneField(Listanft, models.CASCADE, db_column='IdLis', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'portfolio'
        app_label = 'exhibitions'



class Pripada(models.Model):
    idpri = models.AutoField(db_column='IdPri', primary_key=True)  # Field name made lowercase.
    idlis = models.OneToOneField(Listanft, models.CASCADE, db_column='IdLis')  # Field name made lowercase. The composite primary key (IdLis, IdNFT) found, that is not supported. The first column is selected.
    idnft = models.OneToOneField(Nft, models.CASCADE, db_column='IdNFT')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'pripada'
        app_label = 'exhibitions'




