from datetime import datetime

from django.db import models


class Organization(models.Model):
    organization = models.CharField(max_length=100, unique=True)
    comments = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.organization

    class Meta:
        ordering = ['organization']


class PaymentAccount(models.Model):
    account = models.CharField(max_length=50, unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=False, null=False)
    is_cash = models.BooleanField(blank=False)
    currency = models.ForeignKey('Currencies', on_delete=models.PROTECT, blank=False, null=False)
    open_date = models.DateField(blank=False)
    open_balance = models.DecimalField(max_digits=15, decimal_places=2, blank=False, default=0.00)
    comments = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.account

    class Meta:
        ordering = ['organization', 'account']
        verbose_name = 'Payment account'
        verbose_name_plural = 'Payment accounts'


class Project(models.Model):
    project = models.CharField(max_length=100, unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=False)
    comments = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.project

    class Meta:
        ordering = ['organization', 'project']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'



class Counterparties(models.Model):
    counterparty = models.CharField(max_length=100, unique=True)
    suppliers = models.BooleanField(blank=False)
    customer = models.BooleanField(blank=False)
    employee = models.BooleanField(blank=False)
    other = models.BooleanField(blank=False)
    comments = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.counterparty

    class Meta:
        ordering = ['counterparty']
        verbose_name = 'Counterparty'
        verbose_name_plural = 'Counterparties'


class Currencies(models.Model):
    currency = models.CharField(max_length=10, unique=True)
    code = models.CharField(max_length=3, blank=False)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ['currency']
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'


class CurrenciesRates(models.Model):
    date = models.DateField(blank=False)
    accounting_currency = models.ForeignKey(Currencies, related_name='cur1', on_delete=models.CASCADE, blank=True, null=True)
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE, related_name='cur2', blank=True, null=True)
    rate = models.DecimalField(max_digits=15, decimal_places=6, blank=False, default=0.00)

    def __str__(self):
        return f'{self.accounting_currency}, {self.currency}, {self.date}, {self.rate}'

    class Meta:
        ordering = ['date', 'accounting_currency', 'currency']
        verbose_name = 'Rate'
        verbose_name_plural = "Currency rates"


class TypeCF(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

    class Meta:
        ordering = ['id']
        verbose_name = 'Type CF'
        verbose_name_plural = "Types CF"