# Generated by Django 2.1.1 on 2021-11-09 10:05

from django.db import migrations
import djongo.models.fields
import farmer.models


class Migration(migrations.Migration):

    dependencies = [
        ('farmer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='name',
        ),
        migrations.AddField(
            model_name='categories',
            name='en',
            field=djongo.models.fields.EmbeddedField(model_container=farmer.models.CategoryField, null=True),
        ),
        migrations.AddField(
            model_name='categories',
            name='gu',
            field=djongo.models.fields.EmbeddedField(model_container=farmer.models.CategoryField, null=True),
        ),
    ]
