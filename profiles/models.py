from django.db import models
from accounts.models import Korisnik
class Kolekcionar(models.Model):
    idkor = models.OneToOneField('Registrovanikorisnik', models.CASCADE, db_column='IdKor', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'kolekcionar'
        app_label = 'profiles'


class Kreator(models.Model):
    idkor = models.OneToOneField('Registrovanikorisnik', models.CASCADE, db_column='IdKor', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed =  True
        db_table = 'kreator'
        app_label = 'profiles'



class Kupac(models.Model):
    idkor = models.OneToOneField('Registrovanikorisnik', models.CASCADE, db_column='IdKor', primary_key=True)

    class Meta:
        managed =  True
        db_table = 'kupac'
        app_label = 'profiles'

class Registrovanikorisnik(models.Model):
    idkor = models.OneToOneField(Korisnik, models.CASCADE, db_column='IdKor', primary_key=True)  # Field name made lowercase.
    ime = models.CharField(db_column='Ime', max_length=20)  # Field name made lowercase.
    prezime = models.CharField(db_column='Prezime', max_length=20)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
    brojtelefona = models.CharField(db_column='BrojTelefona', max_length=20)  # Field name made lowercase.
    datumrodjenja = models.DateTimeField(db_column='DatumRodjenja')  # Field name made lowercase.
    mestorodjenja = models.CharField(db_column='MestoRodjenja', max_length=20)  # Field name made lowercase.
    brojkartice = models.DecimalField(db_column='BrojKartice', max_digits=10, decimal_places=0)  # Field name made lowercase.
    slika = models.ImageField(db_column='Slika',upload_to='profile_images/', default='profile_images/default.jpg')
    prodatihNFT = models.IntegerField(default=0, db_column='prodatihNft')
    kupljenihNFT = models.IntegerField(default=0, db_column='kupljenihNft')
    datumkreiranja = models.DateField(db_column='DatumKreiranja', null=True, blank=True)  # New field for account creation date

    class Meta:
        managed =  True
        db_table = 'registrovanikorisnik'
        app_label = 'profiles'

