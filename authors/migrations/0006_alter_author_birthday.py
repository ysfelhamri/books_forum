# Generated by Django 5.0.7 on 2024-07-24 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0005_author_book_author_books'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
    ]
