from django.db import models

from directory.models import Organization, PaymentAccount, Project, Counterparties, Currencies


class ExpenseGroup(models.Model):
    expense_group = models.CharField(max_length=50)
    comments = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.expense_group

    class Meta:
        ordering = ['expense_group']
        verbose_name = 'Expense group'
        verbose_name_plural = 'Expense groups'


class ExpensesItem(models.Model):
    expense_item = models.CharField(max_length=50)
    expense_group = models.ForeignKey(ExpenseGroup, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.expense_item

    class Meta:
        ordering = ['expense_group', 'expense_item']
        verbose_name = 'Expense item'
        verbose_name_plural = 'Expense items'


class Payments(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=True, null=True)
    date = models.DateField(blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    account = models.ForeignKey(PaymentAccount, on_delete=models.PROTECT, blank=True)
    currency = models.ForeignKey(Currencies, on_delete=models.PROTECT, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=True, null=True)
    counterparty = models.ForeignKey(Counterparties, on_delete=models.PROTECT, blank=True)
    item = models.ForeignKey(ExpensesItem, on_delete=models.PROTECT, blank=True)
    comments = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.date}, {self.counterparty}, {self.item}, {self.amount}, {self.currency}'

    class Meta:
        ordering = ['organization', 'date', 'item']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def get_absolute_url(self):
        return '/payments'


class PaymentsPlan(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=True, null=True)
    date = models.DateField(blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.ForeignKey(Currencies, on_delete=models.PROTECT, blank=True)
    is_cash = models.BooleanField(blank=False, null=True, default=False)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=False, null=True)
    counterparty = models.ForeignKey(Counterparties, on_delete=models.PROTECT, blank=True)
    item = models.ForeignKey(ExpensesItem, on_delete=models.PROTECT, blank=True)
    comments = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.date}, {self.counterparty}, {self.item}, {self.amount}'

    class Meta:
        ordering = ['date', 'item']
        verbose_name = 'Payment plan'
        verbose_name_plural = 'Payments plan'

    def get_absolute_url(self):
        return '/payments_plan'