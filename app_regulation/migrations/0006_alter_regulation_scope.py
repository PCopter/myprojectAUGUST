# Generated by Django 5.0.7 on 2024-08-10 02:20

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_regulation', '0005_country_image_relative_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regulation',
            name='scope',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
