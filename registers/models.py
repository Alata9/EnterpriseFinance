from django.db import models

from directory.models import *


class Rates(models.Model):
    currency = models.ForeignKey(Currenсies, on_delete=models.PROTECT, blank=True)
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