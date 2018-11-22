# -*- coding: UTF-8 -*-
# Copyright 2014 Rumma & Ko Ltd
# This file is part of the Lino Welfare project.
# Lino Welfare is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino Welfare is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino Welfare; if not, see <http://www.gnu.org/licenses/>.

"""

.. management_command:: gd2lino

Load pcsw.Clients from tab-separated plain text file.

"""

from builtins import map
import os
import datetime

from dateutil import parser as dateparser

from django.conf import settings
from django.core.management import call_command
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from lino_xl.lib.contacts.utils import name2kw, street2kw
from lino.utils import join_words
from lino.utils.instantiator import Instantiator

from lino.api import dd, rt
from lino.api import rt
from lino.utils import camelize

from lino.core.utils import app_labels
from lino_xl.lib.beid.mixins import BeIdCardTypes



class CsvLoader(object):
    field_sep = '\t'
    fields = None

    def __init__(self):
        if isinstance(self.fields, basestring):
            self.fields = self.fields.split()

    def load(self, filename):
        n = 0
        count = 0
        for ln in file(filename).readlines():
            ln = ln.decode("utf-8")
            n += 1
            ln = ln.strip()
            if not ln:
                continue
            values = ln.split('\t')
            if len(values) != len(self.fields):
                dd.logger.warning(
                    "Ignored line %d : invalid number of fields", n)
                continue
            kw = dict()
            for i, v in enumerate(values):
                kw[self.fields[i]] = v
            self.process_line(kw)
            count += 1
        dd.logger.info("%d lines have been processed.", count)

    def process_line(self, kw):
        raise NotImplementedError()




class GDLoader(CsvLoader):
    fields = 'a a a gesdos_id last_name first_name birth_date a nation aaaamm a a'

    def process_line(self, kw):
        del kw['a']
        bd = kw['birth_date']
        a = bd.split('/')
        if len(a) != 3:
            dd.logger.info("Ignored invalid birth_date %s.", )
            return
        a = map(int, a)
        d = datetime.date(a[2], a[1], a[0])
        kw['birth_date'] = d

        aaaamm = kw.pop('aaaamm')
        kw['created'] = datetime.date(int(aaaamm[:4]), int(aaaamm[-2:]), 1)
        kw['first_name'] = camelize(kw['first_name'])
        kw['last_name'] = camelize(kw['last_name'])

        Country = rt.models.countries.Country
        Client = rt.models.pcsw.Client
        nation = kw.pop('nation').strip()

        if nation:
            try:
                country = Country.objects.get(inscode=nation)
                kw.update(nationality=country)
            except Country.DoesNotExist:
                dd.logger.warning("No Country with INS %s", nation)
            # except Country.MultipleObjectsReturned:
            #     dd.logger.warning("No Country with INS %s", nation)

        obj = Client(**kw)
        if not obj.gesdos_id:
            raise Exception("20140312")

        try:
            current = Client.objects.get(gesdos_id=obj.gesdos_id)
            # dd.logger.info("Existing %s", obj)
            for k in 'birth_date first_name last_name nationality'.split():
                setattr(current, k, getattr(obj, k))
            obj = current
        except Client.DoesNotExist:
            # dd.logger.info("New client %s", obj)
            pass

        obj.full_clean()
        obj.save()
        dd.logger.info("%s has been imported.", dd.obj2str(obj))


class Command(BaseCommand):
    args = '<path_to_tim_data_dir>'
    help = 'Performs a database reset and initial import of your TIM data'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError(
                'Please specify the path to the data file to import!')
        loader = GDLoader()
        for arg in args:
            loader.load(arg)

