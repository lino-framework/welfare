"""
Adds models like Study, Experience, ... 
which contain data for printing a CV 
for a Client.
"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "Ceci n'est pas une documentation."
    verbose_name = _("Career")  # _("CV")

    ## settings
    person_model = 'pcsw.Client'
