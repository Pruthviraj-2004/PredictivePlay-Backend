# Generated by Django 5.1.5 on 2025-02-07 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictiveplayapp', '0003_winnermatchdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='status',
            field=models.IntegerField(choices=[(0, 'Upcoming'), (1, 'Ongoing'), (2, 'Completed')], default=0),
        ),
    ]
