# Generated by Django 4.2.13 on 2024-05-21 00:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0004_registrovanikorisnik_datumkreiranja'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kolekcionar',
            name='idkor',
            field=models.OneToOneField(db_column='IdKor', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='profiles.registrovanikorisnik'),
        ),
        migrations.AlterField(
            model_name='kreator',
            name='idkor',
            field=models.OneToOneField(db_column='IdKor', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='profiles.registrovanikorisnik'),
        ),
        migrations.AlterField(
            model_name='kupac',
            name='idkor',
            field=models.OneToOneField(db_column='IdKor', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='profiles.registrovanikorisnik'),
        ),
        migrations.AlterField(
            model_name='registrovanikorisnik',
            name='idkor',
            field=models.OneToOneField(db_column='IdKor', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
