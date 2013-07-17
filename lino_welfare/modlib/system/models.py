# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
## This file is part of the Lino-Faggio project.
## Lino-Faggio is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino-Faggio is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino-Faggio; if not, see <http://www.gnu.org/licenses/>.

"""
This module extends :mod:`lino.modlib.cal.models`
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino import dd

from lino.modlib.system.models import *


class Signers(dd.Model):
    """
    Model mixin which adds two fields `signer1` and `signer2`,
    the two in-house signers of contracts and official documents.
    
    Inherited by :class:`SiteConfig <lino.modlib.system.models.SiteConfig>` 
    and :class:`ContractBase`.
    """
    
    class Meta:
        abstract = True
        
    signer1 = models.ForeignKey("contacts.Person",
      related_name="%(app_label)s_%(class)s_set_by_signer1",
      #~ default=default_signer1,
      verbose_name=_("Secretary"))
      
    signer2 = models.ForeignKey("contacts.Person",
      related_name="%(app_label)s_%(class)s_set_by_signer2",
      #~ default=default_signer2,
      verbose_name=_("President"))
      
    @chooser()
    def signer1_choices(cls):
        sc = settings.SITE.site_config
        kw = dict()
        if sc.signer1_function:
            kw.update(rolesbyperson__type=sc.signer1_function)
        return settings.SITE.modules.contacts.Person.objects.filter(
              rolesbyperson__company=sc.site_company,**kw)
        
    @chooser()
    def signer2_choices(cls):
        sc = settings.SITE.site_config
        kw = dict()
        if sc.signer2_function:
            kw.update(rolesbyperson__type=sc.signer2_function)
        return settings.SITE.modules.contacts.Person.objects.filter(
              rolesbyperson__company=sc.site_company,**kw)
      
  


class SiteConfig(SiteConfig,Signers):
    """
    This adds the :class:`lino_welfare.modlib.isip.models.Signers` 
    mixin to Lino's standard SiteConfig.
    
    """
        
    signer1_function = dd.ForeignKey("contacts.RoleType",
            blank=True,null=True,
            verbose_name=_("First signer function"),
            help_text=_("""Contact function to designate the secretary."""),
            related_name="%(app_label)s_%(class)s_set_by_signer1")
    signer2_function = dd.ForeignKey("contacts.RoleType",
            blank=True,null=True,
            verbose_name=_("Second signer function"),
            help_text=_("Contact function to designate the president."),
            related_name="%(app_label)s_%(class)s_set_by_signer2")
            
       

dd.update_field(SiteConfig,'signer1', blank=True,null=True)
dd.update_field(SiteConfig,'signer2', blank=True,null=True)

