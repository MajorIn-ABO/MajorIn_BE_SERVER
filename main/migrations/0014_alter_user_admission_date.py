# Generated by Django 4.2.6 on 2024-05-10 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_user_user_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='admission_date',
            field=models.IntegerField(),
        ),
    ]
