# Generated by Django 4.1.2 on 2022-10-29 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='カテゴリ名')),
            ],
        ),
        migrations.CreateModel(
            name='IncomeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='カテゴリ名')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentCardCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='カードカテゴリ名')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='カテゴリ名')),
            ],
        ),
        migrations.CreateModel(
            name='Rest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='日付')),
                ('rest', models.IntegerField(verbose_name='金額')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kakeiboapp.bankcategory', verbose_name='銀行')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日付')),
                ('price', models.IntegerField(verbose_name='金額')),
                ('description', models.TextField(blank=True, null=True, verbose_name='概要')),
                ('cardcategory', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kakeiboapp.paymentcardcategory', verbose_name='カードカテゴリ名')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kakeiboapp.paymentcategory', verbose_name='カテゴリ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日付')),
                ('price', models.IntegerField(verbose_name='金額')),
                ('description', models.TextField(blank=True, null=True, verbose_name='概要')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kakeiboapp.incomecategory', verbose_name='カテゴリ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
        ),
    ]
