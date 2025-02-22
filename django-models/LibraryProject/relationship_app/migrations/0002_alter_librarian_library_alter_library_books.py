# Generated by Django 5.1.6 on 2025-02-22 11:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relationship_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='librarian',
            name='library',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='librarian', to='relationship_app.library'),
        ),
        migrations.AlterField(
            model_name='library',
            name='books',
            field=models.ManyToManyField(related_name='libraries', to='relationship_app.book'),
        ),
    ]
