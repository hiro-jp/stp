# Generated by Django 2.2.3 on 2019-08-16 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stp', '0002_item_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_approved',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='date_dispatched',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='date_placed',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='tracking_number',
            field=models.CharField(max_length=20, null=True),
        ),
    ]