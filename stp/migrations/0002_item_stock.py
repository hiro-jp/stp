# Generated by Django 2.2.3 on 2019-08-16 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='stock',
            field=models.IntegerField(default=0),
        ),
    ]
