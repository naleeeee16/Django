from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, user_type='guest', **extra_fields):
        if not username:
            raise ValueError('Korisničko ime je obavezno')

        user = self.model(username=username, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password, user_type='admin')
        user.is_admin = True
        user.save(using=self._db)
        adm = Administrator(idkor=user)
        adm.save()
        return user

class Korisnik(AbstractBaseUser):
    idkor = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, unique=True)
    user_type = models.CharField(max_length=20, default='guest')  # Dodajte polje za tip korisnika

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'



    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin



class Administrator(models.Model):
    idkor = models.OneToOneField('Korisnik', models.DO_NOTHING, db_column='IdKor',
                                 primary_key=True)  # Field name made lowercase.
    class Meta:
        managed = True
        db_table = 'administrator'
        app_label = 'accounts'


class Zahtevzaregistraciju(models.Model):
    idzah = models.AutoField(db_column='IdZah', primary_key=True)  # Field name made lowercase.
    korime = models.CharField(db_column='KorIme', max_length=32, default='' ) # Field name made lowercase.
    sifra = models.CharField(db_column='Sifra', max_length=128, null=True)  # Field name made lowercase. Povećan max_length zbog hesirane šifre.
    ime = models.CharField(db_column='Ime', max_length=20)  # Field name made lowercase.
    prezime = models.CharField(db_column='Prezime', max_length=20)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
    brojtelefona = models.CharField(db_column='BrojTelefona', max_length=20)  # Field name made lowercase.
    datumrodjenja = models.DateField(db_column='DatumRodjenja')  # Field name made lowercase.
    mestorodjenja = models.CharField(db_column='MestoRodjenja', max_length=20)  # Field name made lowercase.
    brojkartice = models.CharField(db_column='BrojKartice', max_length=10)  # Field name made lowercase.
    uloga = models.CharField(db_column='Uloga', max_length=11, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'zahtevzaregistraciju'
        app_label = 'accounts'


