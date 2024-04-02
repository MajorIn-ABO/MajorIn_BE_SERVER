# Generated by Django 4.2.6 on 2024-04-02 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_usedbooktrade_usedbooktrade_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsedbooktradeData',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('sell_date', models.DateTimeField(auto_now_add=True, verbose_name='판매일')),
                ('sellerid', models.ForeignKey(db_column='sellerid', on_delete=django.db.models.deletion.CASCADE, to='main.user')),
                ('trade', models.ForeignKey(db_column='tradeid', on_delete=django.db.models.deletion.CASCADE, to='main.usedbooktrade')),
            ],
        ),
    ]
