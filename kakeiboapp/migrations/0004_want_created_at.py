# Generated by Django 4.1.2 on 2022-11-20 12:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kakeiboapp', '0003_rename_date_buy_want_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='want',
            name='created_at',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='日付'),
        ),
    ]
