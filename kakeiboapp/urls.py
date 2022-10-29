from django.urls import path
from . import views

app_name = "kakeiboapp"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('payment_list', views.PaymentList.as_view(), name='payment_list'),
    path('income_list/', views.IncomeList.as_view(), name='income_list'),
    path('rest_list/', views.RestList.as_view(), name='rest_list'),
    path('payment_create/', views.PaymentCreate.as_view(), name='payment_create'),
    path('income_create/', views.IncomeCreate.as_view(), name='income_create'),
    path('rest_create/', views.RestCreate.as_view(), name='rest_create'),
    path('payment_update/<int:pk>/', views.PaymentUpdate.as_view(), name='payment_update'),
    path('income_update/<int:pk>/', views.IncomeUpdate.as_view(), name='income_update'),
    path('rest_update/<int:pk>/', views.RestUpdate.as_view(), name='rest_update'),
    path('payment_delete/<int:pk>/', views.PaymentDelete.as_view(), name='payment_delete'),
    path('income_delete/<int:pk>/', views.IncomeDelete.as_view(), name='income_delete'),
    path('month_dashboard/<int:year>/<int:month>/', views.MonthDashboard.as_view(), name='month_dashboard'),
    path('transition/', views.TransitionView.as_view(), name='transition'),
]