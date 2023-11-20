from django.db import models
import datetime

from directory.models import Organization, Counterparties, Project, Currencies, Items


class Calculations(models.Model):
    FlowDirection = (
        ('Receipts', 'Receipts'),
        ('Payments', 'Payments'),
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
    type_calc = models.CharField(max_length=200, choices=TypeCalculation, blank=True)
    flow = models.CharField(max_length=10, choices=FlowDirection, blank=True)
    name = models.CharField(max_length=100, blank=True, unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=True)
    counterparty = models.ForeignKey(Counterparties, on_delete=models.PROTECT, blank=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=True, null=True)
    is_cash = models.BooleanField(blank=True, default=False)
    currency = models.ForeignKey(Currencies, on_delete=models.PROTECT, blank=True)
    comments = models.CharField(max_length=250, blank=True, null=True)
    item = models.ForeignKey(Items, on_delete=models.PROTECT, blank=True)
    date_first = models.DateField(blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True)
    term = models.IntegerField(blank=True, null=True)
    frequency = models.CharField(max_length=200, choices=Frequency, blank=True, default='monthly', null=True)
    loan_rate = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True, null=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_series_constant(date_first, frequency, term, amount):
        frequency_days = {'annually': 365, 'monthly': 31, 'weekly': 7, 'daily': 1}
        days = frequency_days.get(frequency)
        date_pay = date_first
        number = date_first.day
        data_list = [(date_pay, amount)]
        for i in range(term):
            if frequency in ['weekly', 'daily']:
                date_pay = (date_pay + datetime.timedelta(days=days))
            else:
                date_pay = (date_pay + datetime.timedelta(days=days)).replace(day=number)
            data_list.append((date_pay, amount))
        return data_list

    @staticmethod
    def get_series_differ(date_first, term, loan_rate, amount):
        date_pay = date_first
        number = date_first.day
        debt_pay = amount / term
        balance_owed = amount
        data_list = [
            (date_pay, debt_pay),
            (date_pay, amount * loan_rate / 1200),
        ]

        for i in range(term - 1):
            date_pay = (date_pay + datetime.timedelta(days=31)).replace(day=number)
            balance_owed -= debt_pay
            per_pay = balance_owed * loan_rate / 1200
            data_list.append((date_pay, debt_pay))
            data_list.append((date_pay, per_pay))

        return data_list

    @staticmethod
    def get_series_annuity(date_first, term, loan_rate, amount):
        date_pay = date_first
        number = date_first.day
        annuity = (amount * loan_rate / 1200) / (1 - (1 + loan_rate / 1200) ** (-term))
        balance_owed = amount
        data_list = []

        for i in range(term):
            date_pay = (date_pay + datetime.timedelta(days=31)).replace(day=number)
            per_pay = balance_owed * loan_rate / 1200
            debt_pay = annuity - per_pay
            balance_owed -= debt_pay
            data_list.append((date_pay, debt_pay))
            data_list.append((date_pay, per_pay))

        return data_list


    def create_plan_payments(self):
        existing_plan = PaymentDocumentPlan.objects.filter(calculation=self).order_by('date').all()

        if self.flow == 'Payments':
            item_per = Items.objects.filter(code='outflow from loan percents')
            item_debt = Items.objects.filter(code='outflow by a loan')
        else:
            item_per = Items.objects.filter(code='inflow by borrow percents')
            item_debt = Items.objects.filter(code='inflow from a borrow')

        if self.type_calc == 'constant':
            data_list = self.get_series_constant(self.date_first, self.frequency, self.term, self.amount)
        elif self.type_calc == 'differential':
            data_list = self.get_series_differ(self.date_first, self.term, self.loan_rate, self.amount)
        else:
            data_list = self.get_series_annuity(self.date_first, self.term, self.loan_rate, self.amount)

        for i, data in enumerate(data_list):
            plan = PaymentDocumentPlan(
                calculation=self,
                organization=self.organization,
                currency=self.currency,
                is_cash=self.is_cash,
                project=self.project,
                counterparty=self.counterparty,
                comments=self.comments,
                flow=self.flow,
                date=data[0]
            )
            if self.flow == 'Payments':
                plan.outflow_amount = data[1]
                plan.inflow_amount = 0
                plan.item = self.item
            else:
                plan.outflow_amount = 0
                plan.inflow_amount = data[1]
                plan.item = self.item

            if len(existing_plan) > i:
                plan.id = existing_plan[i].id
            plan.save()

        PaymentDocumentPlan.objects.filter(calculation=self, date__gt=data_list[-1][0]).delete()

    def get_absolute_url(self):
        return '/calculations'


class PaymentDocumentPlan(models.Model):
    FlowDirection = (
        ('Receipts', 'Receipts'),
        ('Payments', 'Payments'),
    )

    flow = models.CharField(max_length=10, choices=FlowDirection, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=True, null=True)
    date = models.DateField(blank=True)
    inflow_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    outflow_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    currency = models.ForeignKey(Currencies, on_delete=models.PROTECT, blank=True)
    is_cash = models.BooleanField(blank=False, default=False)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=False, null=True)
    counterparty = models.ForeignKey(Counterparties, on_delete=models.PROTECT, blank=True)
    item = models.ForeignKey(Items, on_delete=models.PROTECT, blank=True)
    calculation = models.ForeignKey(Calculations, on_delete=models.CASCADE, blank=True, null=True)
    comments = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        ordering = ['organization', 'date', 'item']
        verbose_name = 'Payment-plan document'
        verbose_name_plural = 'Payment-plan documents'
