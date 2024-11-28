# Generated by Django 5.0.7 on 2024-07-22 07:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
        ('characters', '0004_alter_character_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Character_Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character_role', models.IntegerField(choices=[(0, 'Main'), (1, 'Supporting')])),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characters.character')),
            ],
        ),
        migrations.AddField(
            model_name='character',
            name='books',
            field=models.ManyToManyField(through='characters.Character_Book', to='books.book'),
        ),
    ]
