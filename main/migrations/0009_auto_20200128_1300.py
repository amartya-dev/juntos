# Generated by Django 2.2.5 on 2020-01-28 13:00

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_profile_organization_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='about',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
