# Generated by Django 4.2.6 on 2024-05-08 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_usedbooktrade_is_damaged_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('refresh', models.CharField(max_length=50, null=True)),
                ('access', models.CharField(max_length=50, null=True)),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='main.user')),
            ],
        ),
    ]
