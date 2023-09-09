from django.db import models

from directory.models import Currencies, Organization


class AccountSettings(models.Model):
    multiple_organizations = models.BooleanField('Keep records of multiple organizations', blank=False)
    multiple_accounts = models.BooleanField('Use multiple payment accounts', blank=False)
    multiple_currencies = models.BooleanField('Use multiple accounting currencies', blank=False)
    multiple_projects = models.BooleanField('Keep records of projects', blank=False)
    organization_default = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=True)
    accounting_currency = models.ForeignKey(Currencies, on_delete=models.CASCADE, blank=True, null=True)


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

    def currency(self):
        try:
            return self.accounting_currency
        except:
            ...
        return None


# class AccountBalancesSlice(models.Model):
#     account =
#     organization =
#     is_cash =
#     currency =
#     open_date =
#     open_balance =
#     close_date =
#     close_balance =
