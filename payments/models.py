from django.db import models

from directory.models import Organization, PaymentAccount, Currencies, Project, Counterparties, IncomeItem, \
    ExpensesItem, Items
from planning.models import PaymentsPlan, ReceiptsPlan


class PaymentDocuments(models.Model):
    FlowDirection = (
        ('Receipts', 'Receipts'),
        ('Payments', 'Payments'),
    )

    flow = models.CharField(max_length=10, choices=FlowDirection, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=False)
    date = models.DateField(blank=False)
    inflow_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=False)
    outflow_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=False)
    account = models.ForeignKey(PaymentAccount, on_delete=models.PROTECT, blank=False)
    currency = models.ForeignKey(Currencies, on_delete=models.PROTECT, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=True, null=True)
    counterparty = models.ForeignKey(Counterparties, on_delete=models.PROTECT, blank=False)
    item = models.ForeignKey(Items, on_delete=models.PROTECT, blank=False)
    comments = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        if self.flow == 'Receipts':
            amount = self.inflow_amount
        else:
            amount = self.outflow_amount
        return f'{self.date}, {self.counterparty}, {self.item}, {amount}, {self.currency}, {self.flow}'


    class Meta:
        ordering = ['flow', 'organization', 'date', 'item']
        verbose_name = 'Payment document'
        verbose_name_plural = 'Payment documents'

    def get_absolute_url(self):
        return '/payments'


class Receipts(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=False)
    date = models.DateField(blank=False)
    amount = models.DecimalField(max_digits=15, decimal_places=2, blank=False)
    account = models.ForeignKey(PaymentAccount, on_delete=models.PROTECT, blank=False)
    currency = models.ForeignKey(Currencies, on_delete=models.PROTECT, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=True, null=True)
    counterparty = models.ForeignKey(Counterparties, on_delete=models.PROTECT, blank=False)
    item = models.ForeignKey(IncomeItem, on_delete=models.PROTECT, blank=False)
    comments = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.date}, {self.counterparty}, {self.item}, {self.amount} {self.currency}'

    @classmethod
    def from_plan(cls, plan_id):
        obj = ReceiptsPlan.objects.get(pk=plan_id)
        return cls(
            organization=obj.organization,
            date=obj.date,
            amount=obj.amount,
            currency=obj.currency,
            project=obj.project,
            counterparty=obj.counterparty,
            item=obj.item,
            comments=obj.comments
        )

    @classmethod
    def from_change(cls, change_id):
        obj = ChangePayAccount.objects.get(pk=change_id)
        return cls(
            organization=obj.organization,
            date=obj.date,
            account=obj.pay_account_to,
            amount=obj.amount,
            currency=obj.currency,

            comments='Change payment account'
        )

    class Meta:
        ordering = ['organization', 'date', 'item']
        verbose_name = 'Receipt'
        verbose_name_plural = 'Receipts'

    def get_absolute_url(self):
        return '/payments'


class Payments(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=True, null=True)
    date = models.DateField(blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    account = models.ForeignKey(PaymentAccount, on_delete=models.PROTECT, blank=True)
    currency = models.ForeignKey(Currencies, on_delete=models.PROTECT, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=True, null=True)
    counterparty = models.ForeignKey(Counterparties, on_delete=models.PROTECT, blank=True)
    item = models.ForeignKey(ExpensesItem, on_delete=models.PROTECT, blank=True)
    by_request = models.ForeignKey(PaymentsPlan, on_delete=models.PROTECT, blank=False, null=True)
    comments = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.date}, {self.counterparty}, {self.item}, {self.amount}, {self.currency}'

    @classmethod
    def from_plan(cls, plan_id):
        obj = PaymentsPlan.objects.get(pk=plan_id)
        return cls(
            organization=obj.organization,
            date=obj.date,
            amount=obj.amount,
            currency=obj.currency,
            project=obj.project,
            counterparty=obj.counterparty,
            item=obj.item,
            comments=obj.comments
        )


    class Meta:
        ordering = ['organization', 'date', 'item']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def get_absolute_url(self):
        return '/payments'


class ChangePayAccount(models.Model):
    pay_account_from = models.ForeignKey(PaymentAccount, related_name='account1', on_delete=models.PROTECT, blank=False)
    pay_account_to = models.ForeignKey(PaymentAccount, related_name='account2', on_delete=models.PROTECT, blank=False)
    date = models.DateField(blank=False)
    amount = models.DecimalField(max_digits=15, decimal_places=2, blank=False)
    currency = models.ForeignKey(Currencies, on_delete=models.PROTECT, blank=False)

    def __str__(self):
        return f'{self.date}, {self.pay_account_from}, {self.pay_account_to}, {self.amount}, {self.currency}'

    class Meta:
        ordering = ['date', 'pay_account_from', 'pay_account_to']
        verbose_name = 'Change payment account'
        verbose_name_plural = 'Changes payment account'

    def get_absolute_url(self):
        return '/change_payaccounts'