# Generated by Django 3.1.7 on 2021-03-23 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210323_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fryzjer',
            name='salon',
            field=models.ManyToManyField(null=True, to='main.Salon'),
        ),
    ]
