# Generated by Django 4.2.22 on 2025-06-05 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        ('startups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='startup',
            field=models.ForeignKey(db_column='startup_id', on_delete=django.db.models.deletion.CASCADE, to='startups.startupprofile'),
        ),
    ]
