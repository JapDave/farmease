# Generated by Django 2.1.1 on 2021-11-18 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmer', '0003_auto_20211113_0749'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmer',
            name='status',
            field=models.CharField(default=None, max_length=50, verbose_name='Status'),
        ),
    ]
