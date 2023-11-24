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
    debit = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, blank=True, null=True)
    credit = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, blank=True, null=True)
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
        ('New_projects', 'New projects'),
    )

    Activities = (
        ('operating', 'operating'),
        ('financing', 'financing'),
        ('investing', 'investing'),
    )

    @classmethod
    def get_activity(cls, group):
        activities = {
            'operating': [cls.ItemGroups[0], cls.ItemGroups[1], cls.ItemGroups[2],
                          cls.ItemGroups[3], cls.ItemGroups[4], cls.ItemGroups[5]],
            'financing': [cls.ItemGroups[6]],
            'investing': [cls.ItemGroups[7], cls.ItemGroups[8]],
        }
        return [k for k in activities if set(activities[k]) & {group}]

    name = models.CharField(max_length=100, unique=True, blank=True, null=True)             # user enters
    code = models.CharField(max_length=100, unique=True, blank=True, null=True)             # system name, add initially
    group = models.CharField(max_length=100, choices=ItemGroups, blank=False)               # user enters
    flow = models.CharField(max_length=10, choices=FlowDirection, blank=True)               # auto-adding
    activity = models.CharField(max_length=10, choices=Activities, blank=True, null=True)   # auto-adding


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['group', 'name']
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def get_absolute_url(self):
        return '/items'


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
