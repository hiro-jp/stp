# Generated by Django 2.2.3 on 2019-07-12 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stp', '0012_auto_20190712_1215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
    ]