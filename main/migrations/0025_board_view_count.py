# Generated by Django 4.2.6 on 2024-06-13 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_rename_keep_board_bookmark'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='view_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]