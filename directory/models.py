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
    comments = models.CharField(max_length=100, blank=True, null=True)
    suppliers = models.BooleanField(blank=True, default=False)
    customer = models.BooleanField(blank=True, default=False)
    employee = models.BooleanField(blank=True, default=False)
    other = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.counterparty

    class Meta:
        ordering = ['counterparty']
        verbose_name = 'Counterparty'
        verbose_name_plural = 'Counterparties'


class InitialDebts(models.Model):
    TypeDebts = (
        ('', ''),
        ('Lender', 'Lender'),
        ('Borrower', 'Borrower'),
        ('Other', 'Other'),
    )

    counterparty = models.ForeignKey(Counterparties, on_delete=models.PROTECT, blank=False)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=False)
    debit = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    credit = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    comments = models.CharField(max_length=250, blank=True, null=True)
    currency = models.ForeignKey('Currencies', on_delete=models.PROTECT, blank=False)
    type_debt = models.CharField(max_length=10, choices=TypeDebts, blank=False)

    def __str__(self):
        return f'{self.counterparty}, {self.organization}, {self.type_debt}, DR: {self.debit}, CR: {self.credit}, {self.currency}'

    class Meta:
        ordering = ['counterparty', 'organization']
        verbose_name = 'Counterparty initial debts'
        verbose_name_plural = 'Counterparties initial debts'


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


class Items(models.Model):
    FlowDirection = (
        ('Receipts', 'Receipts'),
        ('Payments', 'Payments'),
    )
    ItemGroups = (
        ('Sales_income', 'Sales income'),
        ('Direct_expenses', 'Direct expenses'),
        ('Administrative_expenses', 'Administrative expenses'),
        ('Commercial_expenses', 'Commercial expenses'),
        ('Production_costs', 'Production costs'),
        ('Other', 'Other income and expenses'),
        ('Loans', 'Credits and loans'),
        ('Fixed_assets', 'Fixed assets'),
        ('Other_noncurrent_assets', 'Other noncurrent assets'),
        ('New_projects', 'New projects'),
    )

    item = models.CharField(max_length=100, unique=True)
    flow = models.CharField(max_length=10, choices=FlowDirection, blank=True)
    group = models.CharField(max_length=100, choices=ItemGroups, blank=True)

    def __str__(self):
        return self.item

    class Meta:
        ordering = ['group', 'item']
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def get_absolute_url(self):
        return '/items'


#-------------------for delete-------------------------------

class TypeCF(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

    class Meta:
        ordering = ['id']
        verbose_name = 'Activities'
        verbose_name_plural = "Activities"


class IncomeGroup(models.Model):
    income_group = models.CharField(max_length=50)
    comments = models.CharField(max_length=255, blank=True, null=True)
    type_cf = models.ForeignKey(TypeCF, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.income_group

    class Meta:
        ordering = ['type_cf', 'income_group']
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