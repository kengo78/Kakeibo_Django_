from django.contrib import admin
from .models import Payment, Income, PaymentCategory, IncomeCategory, Rest, BankCategory, PaymentCardCategory
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class PaymentResource(resources.ModelResource):
    class Meta:
        model = Payment


class PaymentAdmin(ImportExportModelAdmin):
    search_fields = ('description',)
    # list_display = ['date', 'category', 'price', 'cardcategory','description']
    list_display = ['date', 'category', 'price','description']
    list_filter = ('category',)
    ordering = ('-date',)

    resource_class = PaymentResource


class PaymentCategoryResource(resources.ModelResource):
    class Meta:
        model = PaymentCategory


class PaymentCategoryAdmin(ImportExportModelAdmin):
    resource_class = PaymentCategoryResource
    
class PaymentCardCategoryResource(resources.ModelResource):
    class Meta:
        model = PaymentCardCategory


class PaymentCardCategoryAdmin(ImportExportModelAdmin):
    resource_class = PaymentCardCategoryResource


class IncomeResource(resources.ModelResource):
    class Meta:
        model = Income


class IncomeAdmin(ImportExportModelAdmin):
    search_fields = ('description',)
    list_display = ['date', 'category', 'price', 'description']
    list_filter = ('category',)
    ordering = ('-date',)

    resource_class = IncomeResource


class IncomeCategoryResource(resources.ModelResource):
    class Meta:
        model = IncomeCategory


class IncomeCategoryAdmin(ImportExportModelAdmin):
    resource_class = IncomeCategoryResource
    
class RestResource(resources.ModelResource):
    class Meta:
        model = Rest
        
class RestAdmin(ImportExportModelAdmin):
    search_fields = ('category',)
    list_display = ['date', 'rest','category']
    list_filter = ('category',)
    ordering = ('-date',)

    resource_class = RestResource
    
        
class BankCategoryResource(resources.ModelResource):
    class Meta:
        model = BankCategory
        
class BankCategoryAdmin(ImportExportModelAdmin):
    resource_class = BankCategoryResource


admin.site.register(PaymentCategory, PaymentCategoryAdmin)
admin.site.register(PaymentCardCategory, PaymentCardCategoryAdmin)
admin.site.register(IncomeCategory, IncomeCategoryAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Rest, RestAdmin)
admin.site.register(BankCategory, BankCategoryAdmin)