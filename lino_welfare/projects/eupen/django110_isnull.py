from __future__ import print_function
from lino.api.shell import *
Country = rt.models.countries.Country
print(Country.objects.all().count())
print(Country.objects.filter(actual_country__isnull=True).count())
print(Country.objects.filter(actual_country__isnull=False).count())
print(Country.objects.exclude(actual_country__isnull=True).count())
be = Country.objects.get(isocode="BE")
print(type(be.actual_country))
