from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.views import generic
from django.contrib.auth import login
from django.urls import reverse_lazy

from .models import Payment, Income,IncomeCategory, PaymentCategory,Rest
from .forms import PaymentSearchForm, IncomeSearchForm, PaymentCreateForm, IncomeCreateForm, TransitionGraphSearchForm, RestCreateForm 
from django.contrib import messages 
from django.shortcuts import redirect 
from django.utils import timezone

import numpy as np
import pandas as pd
from django_pandas.io import read_frame
from .plugin_plotly import GraphGenerator



class IndexView(generic.TemplateView):
    template_name = "kakeiboapp/index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        TODAY = str(timezone.now()).split('-')
        year = TODAY[0]
        month = TODAY[1]
        next_year, next_month = get_next(year, month)
        prev_year, prev_month = get_prev(year, month)
        
        # objects = Payment.objects.filter(
        #     date__year = year, date__month = month
        # ).order_by("date")
        # total = 0
        # for object in objects:
        #     total += object.price
        #クレカなので先月の利用額
        payments_objects = Payment.objects.filter(
            date__year = year, date__month = prev_month
        ).order_by("date")
        total_payment = 0
        ## 
        for payment_object in payments_objects:
            total_payment += payment_object.price
        
        rest_objects = Rest.objects.order_by("date")
        rest_total = 0
        for object in rest_objects:
            rest_total += object.rest
        usable = rest_total - total_payment
        context = {
            "year": year,
            'month': month,
            # "total": total,
            "payments":payments_objects,
            "total_payment": total_payment,
            "rest": rest_total,
            "next_year": next_year,
            "next_month": next_month,
            "prev_year": prev_year,
            "prev_month": prev_month,
            "usable": usable,
        }
        # if not queryset:
        #     return context
        return context

class PaymentList(generic.ListView):
    template_name = 'kakeiboapp/payment_list.html'
    model = Payment
    ordering = '-date'
    paginate_by = 5

    # 追加
    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = PaymentSearchForm(self.request.GET or None)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            # 何も選択されていないときは0の文字列が入るため、除外
            if year and year != '0':
                queryset = queryset.filter(date__year=year)

            # 何も選択されていないときは0の文字列が入るため、除外
            month = form.cleaned_data.get('month')
            if month and month != '0':
                queryset = queryset.filter(date__month=month)

            # 〇〇円以上の絞り込み
            greater_than = form.cleaned_data.get('greater_than')
            if greater_than:
                queryset = queryset.filter(price__gte=greater_than)
            
            # 〇〇円以下の絞り込み
            less_than = form.cleaned_data.get('less_than')
            if less_than:
                queryset = queryset.filter(price__lte=less_than)
            
            # キーワードの絞り込み
            key_word = form.cleaned_data.get('key_word')
            if key_word:
                # 空欄で区切り、順番に絞る、and検索
                if key_word:
                    for word in key_word.split():
                        queryset = queryset.filter(description__icontains=word)
            
            # カテゴリでの絞り込み
            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)

        return queryset
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = IncomeSearchForm(self.request.GET or None)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            if year and year != '0':
                queryset = queryset.filter(date__year=year)

            month = form.cleaned_data.get('month')
            if month and month != '0':
                queryset = queryset.filter(date__month=month)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # search formを渡す
        context['search_form'] = self.form

        return context
    
class IncomeList(generic.ListView):
    template_name = 'kakeiboapp/income_list.html'
    model = Income
    ordering = '-date'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = PaymentSearchForm(self.request.GET or None)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            # 何も選択されていないときは0の文字列が入るため、除外
            if year and year != '0':
                queryset = queryset.filter(date__year=year)

            # 何も選択されていないときは0の文字列が入るため、除外
            month = form.cleaned_data.get('month')
            if month and month != '0':
                queryset = queryset.filter(date__month=month)

            # 〇〇円以上の絞り込み
            greater_than = form.cleaned_data.get('greater_than')
            if greater_than:
                queryset = queryset.filter(price__gte=greater_than)
            
            # 〇〇円以下の絞り込み
            less_than = form.cleaned_data.get('less_than')
            if less_than:
                queryset = queryset.filter(price__lte=less_than)
            
            # キーワードの絞り込み
            key_word = form.cleaned_data.get('key_word')
            if key_word:
                # 空欄で区切り、順番に絞る、and検索
                if key_word:
                    for word in key_word.split():
                        queryset = queryset.filter(description__icontains=word)
            
            # カテゴリでの絞り込み
            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)

        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = IncomeSearchForm(self.request.GET or None)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            if year and year != '0':
                queryset = queryset.filter(date__year=year)

            month = form.cleaned_data.get('month')
            if month and month != '0':
                queryset = queryset.filter(date__month=month)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form

        return context
    
class RestList(generic.ListView):
    template_name = 'kakeiboapp/rest_list.html'
    model = Rest
    ordering = '-date'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = IncomeSearchForm(self.request.GET or None)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            if year and year != '0':
                queryset = queryset.filter(date__year=year)

            month = form.cleaned_data.get('month')
            if month and month != '0':
                queryset = queryset.filter(date__month=month)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form

        return context
    
class PaymentCreate(generic.CreateView):
    """支出登録"""
    template_name = 'kakeiboapp/register.html'
    model = Payment
    form_class = PaymentCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '支出登録'
        return context

    def get_success_url(self):
        return reverse_lazy('kakeiboapp:payment_list')

    # 追加
    # バリデーション時にメッセージを保存
    def form_valid(self, form):
        self.object = payment = form.save()
        # messages.info(self.request,
        #               f'支出を登録しました\n'
        #               f'日付:{payment.date}\n'
        #               f'カテゴリ:{payment.category}\n'
        #               f'金額:{payment.price}円')
        return redirect(self.get_success_url())
class IncomeCreate(generic.CreateView):
    """収入登録"""
    template_name = 'kakeiboapp/register.html'
    model = Income
    form_class = IncomeCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '収入登録'
        return context

    def get_success_url(self):
        return reverse_lazy('kakeiboapp:income_list')
    
    def form_valid(self, form):
        self.object = income = form.save()
        # messages.info(self.request,
        #               f'収入を登録しました\n'
        #               f'日付:{income.date}\n'
        #               f'カテゴリ:{income.category}\n'
        #               f'金額:{income.price}円')
        return redirect(self.get_success_url())
    
class RestCreate(generic.CreateView):
    """残高登録"""
    template_name = 'kakeiboapp/register.html'
    model = Rest
    form_class = RestCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '残高登録'
        return context

    def get_success_url(self):
        return reverse_lazy('kakeiboapp:rest_list')
    
    def form_valid(self, form):
        self.object = rest = form.save()
        # messages.info(self.request,
        #               f'残高を登録しました\n'
        #               f'日付:{rest.date}\n'
        #               f'カテゴリ:{rest.category}\n'
        #               f'金額:{rest.rest}円')
        return redirect(self.get_success_url())
    
class PaymentUpdate(generic.UpdateView):
    """支出更新"""
    template_name = 'kakeiboapp/register.html'
    model = Payment
    form_class = PaymentCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '支出更新'
        return context

    def get_success_url(self):
        return reverse_lazy('kakeiboapp:payment_list')

    def form_valid(self, form):
        self.object = payment = form.save()
        # messages.info(self.request,
        #               f'支出を更新しました\n'
        #               f'日付:{payment.date}\n'
        #               f'カテゴリ:{payment.category}\n'
        #               f'金額:{payment.price}円')
        return redirect(self.get_success_url())


class IncomeUpdate(generic.UpdateView):
    """収入更新"""
    template_name = 'kakeiboapp/register.html'
    model = Income
    form_class = IncomeCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '収入更新'
        return context

    def get_success_url(self):
        return reverse_lazy('kakeiboapp:income_list')

    def form_valid(self, form):
        self.object = income = form.save()
        # messages.info(self.request,
        #               f'収入を更新しました\n'
        #               f'日付:{income.date}\n'
        #               f'カテゴリ:{income.category}\n'
        #               f'金額:{income.price}円')
        return redirect(self.get_success_url())
    
class RestUpdate(generic.UpdateView):
    """収入更新"""
    template_name = 'kakeiboapp/register.html'
    model = Rest
    form_class = RestCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '残高更新'
        return context

    def get_success_url(self):
        return reverse_lazy('kakeiboapp:rest_list')

    # def form_valid(self, form):
    #     self.object = rest = form.save()
    #     messages.info(self.request,
    #                   f'収入を更新しました\n'
    #                   f'日付:{rest.date}\n'
    #                   f'カテゴリ:{rest.category}\n'
    #                   f'金額:{rest.rest}円')
    #     return redirect(self.get_success_url())


class PaymentDelete(generic.DeleteView):
    """支出削除"""
    template_name = 'kakeiboapp/delete.html'
    model = Payment

    def get_success_url(self):
        return reverse_lazy('kakeiboapp:payment_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '支出削除確認'

        return context

    def delete(self, request, *args, **kwargs):
        self.object = payment = self.get_object()

        payment.delete()
        # messages.info(self.request,
        #               f'支出を削除しました\n'
        #               f'日付:{payment.date}\n'
        #               f'カテゴリ:{payment.category}\n'
        #               f'金額:{payment.price}円')
        return redirect(self.get_success_url())


class IncomeDelete(generic.DeleteView):
    """収入削除"""
    template_name = 'kakeiboapp/delete.html'
    model = Income

    def get_success_url(self):
        return reverse_lazy('kakeiboapp:income_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '収入削除確認'

        return context

    def delete(self, request, *args, **kwargs):
        self.object = income = self.get_object()
        income.delete()
        # messages.info(self.request,
        #               f'収入を削除しました\n'
        #               f'日付:{income.date}\n'
        #               f'カテゴリ:{income.category}\n'
        #               f'金額:{income.price}円')
        return redirect(self.get_success_url())
    
class MonthDashboard(generic.TemplateView):
    """月間支出ダッシュボード"""
    template_name = 'kakeiboapp/month_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # これから表示する年月
        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))
        context['year_month'] = f'{year}年{month}月'

        # 前月と次月をコンテキストに入れて渡す
        if month == 1:
            prev_year = year - 1
            prev_month = 12
        else:
            prev_year = year
            prev_month = month - 1

        if month == 12:
            next_year = year + 1
            next_month = 1
        else:
            next_year = year
            next_month = month + 1
        context['prev_year'] = prev_year
        context['prev_month'] = prev_month
        context['next_year'] = next_year
        context['next_month'] = next_month
        
        # ここから追加
        # paymentモデルをdfにする
        queryset = Payment.objects.filter(date__year=year)
        queryset = queryset.filter(date__month=month)
        # クエリセットが何もない時はcontextを返す
        # 後の工程でエラーになるため
        if not queryset:
            return context
        #データフレーム化
        df = read_frame(queryset,
                        fieldnames=['date', 'price', 'category'])

        # グラフ作成クラスをインスタンス化
        gen = GraphGenerator()

        # pieチャートの素材を作成
        df_pie = pd.pivot_table(df, index='category', values='price', aggfunc=np.sum)
        pie_labels = list(df_pie.index.values)
        pie_values = [val[0] for val in df_pie.values]
        plot_pie = gen.month_pie(labels=pie_labels, values=pie_values)
        context['plot_pie'] = plot_pie

        # テーブルでのカテゴリと金額の表示用。
        # {カテゴリ:金額,カテゴリ:金額…}の辞書を作る
        context['table_set'] = df_pie.to_dict()['price']

        # totalの数字を計算して渡す
        context['total_payment'] = df['price'].sum()

        # 日別の棒グラフの素材を渡す
        df_bar = pd.pivot_table(df, index='date', values='price', aggfunc=np.sum)
        dates = list(df_bar.index.values)
        heights = [val[0] for val in df_bar.values]
        plot_bar = gen.month_daily_bar(x_list=dates, y_list=heights)
        context['plot_bar'] = plot_bar

        return context
    

    
class TransitionView(generic.TemplateView):
    """月毎の収支推移"""
    template_name = 'kakeiboapp/transition.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment_queryset = Payment.objects.all()
        income_queryset = Income.objects.all()
        self.form = form = TransitionGraphSearchForm(self.request.GET or None)
        context['search_form'] = self.form

        graph_visible = None
        # plotlyに渡すデータ
        months_payment = None
        payments = None
        months_income = None
        incomes = None

        if form.is_valid():
            # カテゴリーで絞り込む
            payment_category = form.cleaned_data.get('payment_category')
            payment_cardcategory = form.cleaned_data.get('payment_cardcategory')
            if payment_category:
                payment_queryset = payment_queryset.filter(category=payment_category)
            if payment_cardcategory:
                payment_cardqueryset = payment_queryset.filter(cardcategory=payment_cardcategory)
            income_category = form.cleaned_data.get('income_category')
            if income_category:
                income_queryset = income_queryset.filter(category=income_category)

            # 表示するをグラフ
            graph_visible = form.cleaned_data.get('graph_visible')

        # グラフ表示指定がない、もしくは支出グラフ表示が選択
        if not graph_visible or graph_visible == 'Payment':
            payment_df = read_frame(payment_queryset,
                                    fieldnames=['date', 'price'])
            payment_df['date'] = pd.to_datetime(payment_df['date'])
            payment_df['month'] = payment_df['date'].dt.strftime('%Y-%m')
            payment_df = pd.pivot_table(payment_df, index='month', values='price', aggfunc=np.sum)
            months_payment = list(payment_df.index.values)
            payments = [y[0] for y in payment_df.values]
            
            #カード毎のdf
            # payment_carddf = read_frame(payment_cardqueryset, 
            #                             filednames=['date', 'price'])

        # グラフ表示指定がない、もしくは収入グラフ表示が選択
        if not graph_visible or graph_visible == 'Income':
            income_df = read_frame(income_queryset,
                                   fieldnames=['date', 'price'])
            income_df['date'] = pd.to_datetime(income_df['date'])
            income_df['month'] = income_df['date'].dt.strftime('%Y-%m')
            income_df = pd.pivot_table(income_df, index='month', values='price', aggfunc=np.sum)
            months_income = list(income_df.index.values)
            incomes = [y[0] for y in income_df.values]

        #グラフ生成
        gen = GraphGenerator()
        context['transition_plot'] = gen.transition_plot(x_list_payment=months_payment,
                                                   y_list_payment=payments,
                                                   x_list_income=months_income,
                                                   y_list_income=incomes)

        return context
    
def get_next(year, month):
    year = int(year)
    month = int(month)

    if month==12:
        return str(year + 1), "1"
    else:
        return str(year), str(month+1)

def get_prev(year, month):
    year = int(year)
    month = int(month)
    
    if month == 1:
        return str(year-1), "12"
    else:
        return str(year), str(month-1)