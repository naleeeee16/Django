# Generated by Django 4.2.13 on 2024-05-18 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_registrovanikorisnik_kupljenihnft_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrovanikorisnik',
            name='slika',
            field=models.ImageField(db_column='Slika', default='profile_images/default.jpg', upload_to='profile_images/'),
        ),
    ]