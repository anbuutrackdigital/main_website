# Generated by Django 5.0.7 on 2024-08-10 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Crew', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trafficcrewavailable',
            name='status',
            field=models.CharField(choices=[('vacant', 'Vacant'), ('active', 'Active')], default='vacant', max_length=20),
        ),
    ]
