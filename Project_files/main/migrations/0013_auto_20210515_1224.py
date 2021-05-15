# Generated by Django 3.1.1 on 2021-05-15 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20210510_1820'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalonRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salonID', models.IntegerField(blank=True, null=True)),
                ('wlascicielID', models.IntegerField(blank=True, null=True)),
                ('nazwa_salonu', models.CharField(blank=True, max_length=250, null=True)),
                ('imie_wlasciciela', models.CharField(blank=True, max_length=250, null=True)),
                ('nazwisko_wlasciciela', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='fryzjer',
            name='salon_to_add',
            field=models.ManyToManyField(to='main.SalonRelationship'),
        ),
    ]
