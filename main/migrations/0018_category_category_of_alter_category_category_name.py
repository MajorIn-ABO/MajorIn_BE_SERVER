# Generated by Django 4.2.6 on 2024-05-12 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_user_home_password_check'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_of',
            field=models.CharField(choices=[('COMMUNITY', 'community'), ('STUDY', 'study')], default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=10),
        ),
    ]
