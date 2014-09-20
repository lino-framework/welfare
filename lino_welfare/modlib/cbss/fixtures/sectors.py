# -*- coding: UTF-8 -*-
# Copyright 2012 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Fills the Sectors table using the official data from 
http://www.bcss.fgov.be/binaries/documentation/fr/documentation/general/lijst_van_sectoren_liste_des_secteurs.xls    

"""
from lino import dd, rt
from django.conf import settings
from lino.utils import ucsv
from lino.core.dbutils import resolve_model
from os.path import join, dirname

ENCODING = 'latin1'  # the encoding used by the mdb file
#~ ENCODING = 'utf8'

GERMAN = []
GERMAN.append((17, 1, u'ÖSHZ', u'Öffentliche Sozialhilfezentren'))


def objects():

    Sector = resolve_model('cbss.Sector')

    fn = join(dirname(__file__), 'lijst_van_sectoren_liste_des_secteurs.csv')
    reader = ucsv.UnicodeReader(
        open(fn, 'r'), encoding=ENCODING, delimiter=';')

    headers = reader.next()
    if headers != [u'Sector', u'', u'verkorte naam', u'Omschrijving', u'Abréviation', u'Nom']:
        raise Exception("Invalid file format: %r" % headers)
    reader.next()  # ignore second header line
    code = None
    for row in reader:
        s0 = row[0].strip()
        s1 = row[1].strip()
        #~ if s0 == '17' and s1 == '0':
            # ~ continue #
        if s0 or s1:
            kw = {}
            if len(s0) > 0:
                #~ print repr(row[0])
                code = int(s0)
            kw.update(code=code)
            if row[1]:
                kw.update(subcode=int(row[1]))
            kw.update(
                **dd.babel_values('name', de=row[5], fr=row[5], nl=row[3], en=row[5]))
            kw.update(
                **dd.babel_values('abbr', de=row[4], fr=row[4], nl=row[2], en=row[4]))
            #~ print kw
            yield Sector(**kw)

    #~ if 'de' in settings.SITE.languages:
    info = settings.SITE.get_language_info('de')
    if info:
        for code, subcode, abbr, name in GERMAN:
            sect = Sector.objects.get(code=code, subcode=subcode)
            #~ if settings.SITE.DEFAULT_LANGUAGE == 'de':
            if info.index == 0:
                sect.abbr = abbr
                sect.name = name
            else:
                sect.abbr_de = abbr
                sect.name_de = name
            sect.save()

    # default value for SiteConfig.sector is "CPAS"
    #~ settings.SITE.site_config.sector = Sector.objects.get(code=17,subcode=1)
    #~ settings.SITE.site_config.save()
