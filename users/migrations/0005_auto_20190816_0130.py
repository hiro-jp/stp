# Generated by Django 2.2.3 on 2019-08-16 01:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_dealer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dealer',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='stp.Dealer'),
        ),
    ]
