# Generated by Django 5.0.7 on 2024-08-07 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_regulation', '0003_remove_stakeholder_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regulation',
            name='remark',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
