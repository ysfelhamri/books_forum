# Generated by Django 5.0.7 on 2024-07-29 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0012_alter_book_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='book_stats',
            name='average_score',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='book_stats',
            name='popularity_rank',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='book_stats',
            name='score_distribution',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='book_stats',
            name='score_rank',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='book_stats',
            name='user_statuses',
            field=models.JSONField(default=dict),
        ),
    ]
