from django.db import models

from directory.models import Organization, PaymentAccount, Currencies, Project, Counterparties


class IncomeGroup(models.Model):
    income_group = models.CharField(max_length=50)
    comments = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.income_group

    class Meta:
        ordering = ['income_group']
        verbose_name = 'Income group'
        verbose_name_plural = 'Income groups'

    def get_absolute_url(self):
        return '/income_group'


class IncomeItem(models.Model):
    income_item = models.CharField(max_length=50)
    income_group = models.ForeignKey(IncomeGroup, on_delete=models.PROTECT, blank=True)

    def __str__(self):
        return self.income_item

    class Meta:
        ordering = ['income_group', 'income_item']
        verbose_name = 'Income item'
        verbose_name_plural = 'Income items'

    def get_absolute_url(self):
        return '/income_item'


class Receipts(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=False)
    date = models.DateField(blank=False)
    amount = models.DecimalField(max_digits=15, decimal_places=2, blank=False)
    account = models.ForeignKey(PaymentAccount, on_delete=models.PROTECT, blank=False)
    currency = models.ForeignKey(Currencies, on_delete=models.PROTECT, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=True, null=True)
    counterparty = models.ForeignKey(Counterparties, on_delete=models.PROTECT, blank=False)
    item = models.ForeignKey(IncomeItem, on_delete=models.PROTECT, blank=False)
    comments = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.date}, {self.counterparty}, {self.item}, {self.amount} {self.currency}'

    class Meta:
        ordering = ['organization', 'date', 'item']
        verbose_name = 'Receipt'
        verbose_name_plural = 'Receipts'

    def get_absolute_url(self):
        return '/receipts'


class ReceiptsPlan(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=True, null=True)
    date = models.DateField(blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.ForeignKey(Currencies, on_delete=models.PROTECT, blank=True)
    is_cash = models.BooleanField(blank=False, null=True, default=False)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=False, null=True)
    counterparty = models.ForeignKey(Counterparties, on_delete=models.PROTECT, blank=True)
    item = models.ForeignKey(IncomeItem, on_delete=models.PROTECT, blank=True)
    comments = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.date}, {self.counterparty}, {self.item}, {self.amount}'

    class Meta:
        ordering = ['organization', 'date', 'item']
        verbose_name = 'Receipt plan'
        verbose_name_plural = 'Receipts plan'

    def get_absolute_url(self):
        return '/receipts_plan'
