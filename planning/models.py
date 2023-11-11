from django.db import models

import datetime

from directory.models import Organization, Counterparties, Project, Currencies, ExpensesItem, IncomeItem


class Calculations(models.Model):
    FlowDirection = (
        ('receipts', 'Receipts'),
        ('payments', 'Payments'),
    )

    TypeCalculation = (
        ('constant', 'Constant payments'),
        ('annuity', 'Credit: annuity'),
        ('differential', 'Credit: differentiated'),
    )

    Frequency = (
        ('annually', 'annually'),
        ('monthly', 'monthly'),
        ('weekly', 'weekly'),
        ('daily', 'daily'),
    )
    type_calc = models.CharField(max_length=200, choices=TypeCalculation, default='constant', blank=True)
    flow = models.CharField(max_length=10, choices=FlowDirection, blank=True, default='payments')
    name = models.CharField(max_length=100, blank=True, unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=True)
    counterparty = models.ForeignKey(Counterparties, on_delete=models.PROTECT, blank=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=True, null=True)
    is_cash = models.BooleanField(blank=True, default=False)
    currency = models.ForeignKey(Currencies, on_delete=models.PROTECT, blank=True)
    comments = models.CharField(max_length=250, blank=True, null=True)
    item = models.ForeignKey(ExpensesItem, on_delete=models.PROTECT, blank=True)
    date_first = models.DateField(blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True)
    term = models.IntegerField(blank=True, null=True)
    frequency = models.CharField(max_length=200, choices=Frequency, blank=True, default='monthly', null=True)
    loan_rate = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True, null=True)

    def __str__(self):
        return self.name


    @staticmethod
    def get_series_constant(date_first, frequency, term):
        frequency_days = {'annually': 365, 'monthly': 31, 'weekly': 7, 'daily': 1}
        days = frequency_days.get(frequency)
        date_pay = date_first
        number = date_first.day
        data_list = [date_pay]
        for i in range(term):
            if frequency in ['weekly', 'daily']:
                date_pay = (date_pay + datetime.timedelta(days=days))
            else:
                date_pay = (date_pay + datetime.timedelta(days=days)).replace(day=number)
            data_list.append(date_pay)
        return data_list


    @staticmethod
    def get_series_differ(date_first, term, loan_rate, amount):
        date_pay = date_first
        number = date_first.day
        debt_pay = amount / term                                            # сумма ежемесячного платежа по телу кредита (дифф.плат)
        balance_owed = amount                                               # остаток текущего долга по кредиту
        data_list = [(date_pay, debt_pay, amount * loan_rate / 1200)]
        print(data_list)
        for i in range(term-1):
            date_pay = (date_pay + datetime.timedelta(days=31)).replace(day=number)
            balance_owed -= debt_pay
            per_pay = balance_owed * loan_rate / 1200                       # сумма процентов к уплате
            data_list.append((date_pay, debt_pay, per_pay))
            print(date_pay, debt_pay, per_pay)
        return data_list


    @staticmethod
    def get_series_annuity(date_first, term, loan_rate, amount):
        date_pay = date_first
        number = date_first.day
        annuity = (amount * loan_rate/1200) / (1 - (1 + loan_rate/1200)**(-term))
        balance_owed = amount
        data_list = []
        print(data_list)
        for i in range(term):
            date_pay = (date_pay + datetime.timedelta(days=31)).replace(day=number)
            per_pay = balance_owed * loan_rate / 1200
            debt_pay = annuity - per_pay
            balance_owed -= debt_pay
            data_list.append((date_pay, debt_pay, per_pay))
            print(date_pay, debt_pay, per_pay)
        return data_list


    @classmethod
    def create_plan_payments(cls, create_plan):
        obj = Calculations.objects.get(pk=create_plan)
        existing_plan = PaymentsPlan.objects.filter(calculation=obj).order_by('date').all()
        type_calc = obj.type_calc
        item_debt = ExpensesItem.objects.filter(id=1)  # статья погашения долга
        item_per = ExpensesItem.objects.filter(id=11)  # статья погашения процентов

        if type_calc == 'constant':
            data_list = cls.get_series_constant(obj.date_first, obj.frequency, obj.term)
            for i in range(obj.term):
                plan = PaymentsPlan(
                    calculation=obj,
                    organization=obj.organization,
                    currency=obj.currency,
                    is_cash=obj.is_cash,
                    project=obj.project,
                    counterparty=obj.counterparty,
                    comments=obj.comments,
                    date=data_list[i],
                    item=obj.item,
                    amount=obj.amount
                )
                if len(existing_plan) > i:
                    plan.id = existing_plan[i].id
                plan.save()

        else:
            if type_calc == 'differential':
                data_list = cls.get_series_differ(obj.date_first, obj.term, obj.loan_rate, obj.amount)
            else:
                data_list = cls.get_series_annuity(obj.date_first, obj.term, obj.loan_rate, obj.amount)

            for i in range(obj.term):
                plan_debt = PaymentsPlan(
                    calculation=obj,
                    organization=obj.organization,
                    currency=obj.currency,
                    is_cash=obj.is_cash,
                    project=obj.project,
                    counterparty=obj.counterparty,
                    comments=obj.comments,
                    date=data_list[i][0],
                    item=obj.item,
                    amount=data_list[i][1]
                )
                if len(existing_plan) > i:
                    plan_debt.id = existing_plan[i].id
                plan_debt.save()

            for i in range(obj.term):
                plan_per = PaymentsPlan(
                    calculation=obj,
                    organization=obj.organization,
                    currency=obj.currency,
                    is_cash=obj.is_cash,
                    project=obj.project,
                    counterparty=obj.counterparty,
                    comments=obj.comments,
                    date=data_list[i][0],
                    item=obj.item,
                    amount=data_list[i][2]
                )
                if len(existing_plan) > i:
                    plan_per.id = existing_plan[i].id
                plan_per.save()

        # PaymentsPlan.objects.filter(calculation=obj, date__gte=obj.date_first).delete()


    def get_absolute_url(self):
        return '/calculations'


class PaymentsPlan(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=True, null=True)
    date = models.DateField(blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.ForeignKey(Currencies, on_delete=models.PROTECT, blank=True)
    is_cash = models.BooleanField(blank=False, default=False)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=False, null=True)
    counterparty = models.ForeignKey(Counterparties, on_delete=models.PROTECT, blank=True)
    item = models.ForeignKey(ExpensesItem, on_delete=models.PROTECT, blank=True)
    calculation = models.ForeignKey(Calculations, on_delete=models.PROTECT, blank=True, null=True)
    comments = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.date}, {self.counterparty}, {self.item}, {self.amount}'

    class Meta:
        ordering = ['date', 'item']
        verbose_name = 'Payment plan'
        verbose_name_plural = 'Payments plan'

    def get_absolute_url(self):
        return '/payments_plan'


class ReceiptsPlan(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=True, null=True)
    date = models.DateField(blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.ForeignKey(Currencies, on_delete=models.PROTECT, blank=True)
    is_cash = models.BooleanField(blank=False, default=False)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=False, null=True)
    counterparty = models.ForeignKey(Counterparties, on_delete=models.PROTECT, blank=True)
    item = models.ForeignKey(IncomeItem, on_delete=models.PROTECT, blank=True)
    calculation = models.ForeignKey(Calculations, on_delete=models.PROTECT, blank=True, null=True)
    comments = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.date}, {self.counterparty}, {self.item}, {self.amount}'

    class Meta:
        ordering = ['organization', 'date', 'item']
        verbose_name = 'Receipt plan'
        verbose_name_plural = 'Receipts plan'

    def get_absolute_url(self):
        return '/receipts_plan'


