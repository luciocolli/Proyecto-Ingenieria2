# Generated by Django 5.0.4 on 2024-05-19 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0005_alter_publication_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
