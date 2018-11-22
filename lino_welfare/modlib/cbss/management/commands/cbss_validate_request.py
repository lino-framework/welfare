# -*- coding: UTF-8 -*-
# Copyright 2012 Rumma & Ko Ltd
# This file is part of Lino Welfare.
#
# Lino Welfare is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Welfare is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Welfare.  If not, see
# <http://www.gnu.org/licenses/>.

u"""

This command may be useful if you get an error message 
"A validation error occurred while parsing the request header. 
Please check your message format and content."
It runs a local validation agains the XSD of the request.

In that case, write down the internal ID of your request and 
execute something like the following command in your project 
directory::

  python manage.py cbss_validate_request IdentifyPersonRequest 17
  
Works only for
:class:`SSDN requests <lino_welfare.modlib.cbss.models.SSDNRequest>`.

Background (excerpt from :blogref:`20120603`:

Die fiesteste war eine Fehlermeldung "A validation error occurred while 
parsing the request header. Please check your message format and content."
Die kam durch ein leeres Feld `lino.SiteConfig.site_company.email`.
Aber bevor ich das rausbekommen hatte, habe 
ich mal schnell eine Aktion `validate` geschrieben.
Aber die hing mir dann den Server auf, 
weil sich :term:`lxml` dann mit :term:`mod_wsgi` in die Haare kriegt.
Also sorry: lokales Validieren wird wohl vom Web-Client aus nicht so 
schnell möglich sein. 
Ich könnte einen management command schreiben, 
den man in so einem Fall von einer Shell aus aufrufen könnte. 

"""
from __future__ import print_function

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from lino.api import dd, rt


class Command(BaseCommand):
    args = '<model> <id>'
    help = 'Validate an existing SSDN request against the xsd files.'

    def handle(self, *args, **options):
        model = dd.resolve_model('cbss.' + args[0])
        pk = int(args[1])
        req = model.objects.get(pk=pk)
        req.validate_request()
        #~ print req.logged_messages
        print(req.debug_messages)
