from django.db import models

from directory.models import Organization, PaymentAccount, Project, Counterparties, Currencies, TypeCF


class ExpenseGroup(models.Model):
    expense_group = models.CharField(max_length=50)
    comments = models.CharField(max_length=255, blank=True, null=True)
    type_cf = models.ForeignKey(TypeCF, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.expense_group

    class Meta:
        ordering = ['type_cf', 'expense_group']
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


class Calculations(models.Model):
    TypeCalculation = (
        ('', ''),
        ('constant', 'Constant payments'),
        ('annuity', 'Credit: annuity'),
        ('differential', 'Credit: differentiated'),
    )

    Frequency = (
        ('', ''),
        ('annually', 'annually'),
        ('monthly', 'monthly'),
        ('weekly', 'weekly'),
        ('daily', 'daily'),
    )
    type_calc = models.CharField(max_length=200, choices=TypeCalculation, blank=True)
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
    frequency = models.CharField(max_length=200, choices=Frequency, blank=True, null=True)
    loan_rate = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)



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






