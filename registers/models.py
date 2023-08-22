from django.db import models

from directory.models import Currencies, Organization


class Rates(models.Model):
    currency = models.ForeignKey(Currencies, on_delete=models.PROTECT, blank=True)
    date = models.DateField(blank=True)
    rate = models.DecimalField(max_digits=15, decimal_places=4)

    def __str__(self):
        return f'{self.currency}, {self.date}, {self.rate}'

    class Meta:
        ordering = ['currency', 'date']
        verbose_name = 'Currency rate'
        verbose_name_plural = 'Currency rates'


class AccountSettings(models.Model):
    multiple_organizations = models.BooleanField('Keep records of multiple organizations', blank=False)
    multiple_accounts = models.BooleanField('Use multiple payment accounts', blank=False)
    multiple_currencies = models.BooleanField('Use multiple accounting currencies', blank=False)
    multiple_projects = models.BooleanField('Keep records of projects', blank=False)
    organization_default = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=True)
    # accounting_currency = models.ForeignKey('Main accounting currency', Currencies, on_delete=models.CASCADE,
    #                                         null=True, blank=True)

    def get_absolute_url(self):
        return '/settings'

    @classmethod
    def load(cls):
        try:
            return cls.objects.get(id=1)
        except:
            pass

        return cls(id=1)

    def organization(self):
        try:
            return self.organization_default
        except:
            ...
        return None

    # def currency(self):
    #     try:
    #         return self.accounting_currency
    #     except:
    #         ...
    #     return None