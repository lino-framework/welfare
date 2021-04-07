# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Database fields for `lino_welfare.modlib.debts`.

"""

from __future__ import unicode_literals
from django.db import models

from lino.api import _


class PeriodsField(models.DecimalField):

    """
    Used for `Entry.periods` and `Account.periods`
    (the latter holds simply the default value for the former).
    It means: for how many months the entered amount counts.
    Default value is 1. For yearly amounts set it to 12.
    """

    def __init__(self, *args, **kwargs):
        defaults = dict(
            blank=True,
            default=1,
            help_text=_("""\
For how many months the entered amount counts. 
For example 1 means a monthly amount, 12 a yearly amount."""),
            #~ max_length=3,
            max_digits=3,
            decimal_places=0,
        )
        defaults.update(kwargs)
        super(PeriodsField, self).__init__(*args, **defaults)

#~ class PeriodsField(models.IntegerField):
    #~ """
    #~ Used for `Entry.periods` and `Account.periods`
    #~ (which holds simply the default value for the former).
    #~ It means: for how many months the entered amount counts.
    #~ Default value is 1. For yearly amounts set it to 12.
    #~ """
    #~ def __init__(self, *args, **kwargs):
        #~ defaults = dict(
            #~ max_length=3,
            # max_digits=3,
            #~ blank=True,
            #~ null=True
            #~ )
        #~ defaults.update(kwargs)
        #~ super(PeriodsField, self).__init__(*args, **defaults)


