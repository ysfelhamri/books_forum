# Generated by Django 5.0.7 on 2024-07-25 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_alter_relationship_relationship_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.IntegerField(choices=[(0, 'Completed'), (1, 'Publishing'), (-1, 'On Hiatus')], default=1),
        ),
    ]
