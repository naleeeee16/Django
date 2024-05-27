from django.db import models

from profiles.models import Registrovanikorisnik


# Create your models here.

class Nft(models.Model):
    idnft = models.AutoField(db_column='IdNFT', primary_key=True)  # Field name made lowercase.
    naziv = models.CharField(db_column='Naziv', max_length=20)  # Field name made lowercase.
    vrednost = models.FloatField(db_column='Vrednost')  # Field name made lowercase.
    prosecnaocena = models.DecimalField(db_column='ProsecnaOcena', max_digits=10, decimal_places=0, null=True)  # Field name made lowercase.
    idkre = models.ForeignKey(Registrovanikorisnik, models.SET_NULL, db_column='IdKre', blank=True, null=True)  # Field name made lowercase.
    idvla = models.ForeignKey(Registrovanikorisnik, models.CASCADE, db_column='IdVla', related_name='nft_idvla_set', blank=True, null=True)  # Field name made lowercase.
    opis = models.CharField(db_column='Opis', max_length=256)  # Field name made lowercase.
    slika = models.ImageField(db_column='Slika', upload_to='nft_images/')
    url = models.CharField(db_column='Url', max_length=128)

    class Meta:
        managed =  True
        db_table = 'nft'
        app_label = 'nft'

class Ocena(models.Model):
    idoce = models.AutoField(db_column='IdOce', primary_key=True, default=None)  # Field name made lowercase.
    idkor = models.OneToOneField(Registrovanikorisnik, models.SET_NULL, db_column='IdKor',
                                 null=True)  # Field name made lowercase. The composite primary key (IdKor, IdNFT) found, that is not supported. The first column is selected.
    idnft = models.OneToOneField(Nft, models.CASCADE, db_column='IdNFT')  # Field name made lowercase.
    ocena = models.IntegerField(db_column='Ocena')  # Field name made lowercase.

    class Meta:
        managed =  True
        db_table = 'ocena'
        app_label = 'nft'

