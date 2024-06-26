# Generated by Django 4.2.6 on 2024-05-17 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_usedbooktrade_origin_imgfile_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usedbooktrade',
            name='seller',
        ),
        migrations.RemoveField(
            model_name='usedbooktradedata',
            name='sellerid',
        ),
        migrations.AddField(
            model_name='usedbooktrade',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', default=50, on_delete=django.db.models.deletion.CASCADE, to='main.user', verbose_name='판매자'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usedbooktradedata',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', default=1, on_delete=django.db.models.deletion.CASCADE, to='main.user'),
            preserve_default=False,
        ),
    ]
