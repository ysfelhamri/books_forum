# Generated by Django 5.0.7 on 2024-07-27 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_rating_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='status',
            field=models.IntegerField(choices=[(0, 'Reading'), (1, 'Completed'), (2, 'On-Hold'), (3, 'Dropped'), (4, 'Plan to Read')], default=0),
        ),
    ]
