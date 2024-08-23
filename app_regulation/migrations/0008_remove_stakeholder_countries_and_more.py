# Generated by Django 5.0.7 on 2024-08-16 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_regulation', '0007_remove_regulation_effectivedate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stakeholder',
            name='countries',
        ),
        migrations.AddField(
            model_name='country',
            name='stakeholders_email',
            field=models.ManyToManyField(related_name='countries', to='app_regulation.stakeholder'),
        ),
        migrations.AlterField(
            model_name='regulation',
            name='by',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='regulation',
            name='remark',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
