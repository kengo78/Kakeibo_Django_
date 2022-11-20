from django.db import models
from django.utils import timezone
from accounts.models import User
# Create your models here.
class PaymentCategory(models.Model):#支払いのカテゴリ
    name = models.CharField('カテゴリ名', max_length=16)

    def __str__(self):
        return self.name
    
class PaymentCardCategory(models.Model):
    name = models.CharField('カードカテゴリ名', max_length=16)
    
    def __str__(self):
        return self.name
    
class Payment(models.Model):#支払額
    user = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.PROTECT)
    date = models.DateField('日付')
    price = models.IntegerField('金額')
    category = models.ForeignKey(PaymentCategory, on_delete=models.PROTECT, verbose_name='カテゴリ')
    cardcategory = models.ForeignKey(PaymentCardCategory, on_delete=models.PROTECT, verbose_name='カードカテゴリ名')
    description = models.TextField('概要', null=True, blank=True)


class IncomeCategory(models.Model):
    name = models.CharField('カテゴリ名', max_length=32)

    def __str__(self):
        return self.name


class Income(models.Model):
    user = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.PROTECT)
    date = models.DateField('日付')
    price = models.IntegerField('金額')
    category = models.ForeignKey(IncomeCategory, on_delete=models.PROTECT, verbose_name='カテゴリ')
    description = models.TextField('概要', null=True, blank=True)
    
class BankCategory(models.Model):
    name = models.CharField('カテゴリ名', max_length=32)

    def __str__(self):
        return self.name

class Rest(models.Model):
    user = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.PROTECT)
    date = models.DateField('日付',default=timezone.now)
    rest = models.IntegerField('金額')
    category = models.ForeignKey(BankCategory, on_delete=models.PROTECT,verbose_name='銀行')
    
class Want(models.Model):
    user = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.PROTECT)
    name = models.CharField('名前', max_length=50, blank=False, null=False)
    price = models.IntegerField('金額')
    date_buy = models.DateField('日付')
    