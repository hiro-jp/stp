# Generated by Django 2.2.3 on 2019-08-18 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stp', '0003_auto_20190816_0631'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/%Y/%m/%d', verbose_name='参考画像'),
        ),
    ]
