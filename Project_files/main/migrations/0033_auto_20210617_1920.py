# Generated by Django 3.2 on 2021-06-17 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_auto_20210617_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fryzjer',
            name='srednia_ocena',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salon',
            name='srednia_ocena',
            field=models.FloatField(blank=True, null=True),
        ),
    ]