# Generated by Django 5.0.7 on 2024-07-22 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(0, 'Owner'), (1, 'Admin'), (2, 'Senior Moderator'), (3, 'Moderator'), (4, 'User')], default=4),
        ),
    ]
