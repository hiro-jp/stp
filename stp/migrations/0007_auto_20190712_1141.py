# Generated by Django 2.2.3 on 2019-07-12 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stp', '0006_basketitem_nos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basketitem',
            name='nos',
            field=models.IntegerField(default=0),
        ),
    ]
