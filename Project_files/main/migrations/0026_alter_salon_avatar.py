# Generated by Django 3.2 on 2021-06-17 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_salon_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salon',
            name='avatar',
            field=models.ImageField(default='main/static/ocen_fryzjera/avatars/salony/default-image.jpg', upload_to='main/static/ocen_fryzjera/avatars/salony/'),
        ),
    ]
