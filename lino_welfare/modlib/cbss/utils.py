# -*- coding: UTF-8 -*-
# Copyright 2011-2016 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Utilities for this plugin.
"""

from builtins import str
import os
from lino.api import dd, rt
from lino.utils import join_words

CBSS_ENVS = ('test', 'acpt', 'prod')


def xsdpath(*parts):
    p1 = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(p1, 'XSD', *parts)


def nodetext(node):
    if node is None:
        return ''
    return node.text


def gender2cbss(gender):
    if gender == dd.Genders.male:
        return '1'
    elif gender == dd.Genders.female:
        return '2'
    else:
        return '0'


def cbss2gender(v):
    if v == '1':
        return dd.Genders.male
    elif v == '2':
        return dd.Genders.female
    return None


def cbss2date(s):
    a = s.split('-')
    assert len(a) == 3
    a = [int(i) for i in a]
    return dd.IncompleteDate(*a)


def cbss2civilstate(node):
    value = nodetext(node)
    if not value:
        return value
    v = rt.models.pcsw.CivilState.get_by_value(value)
    # if v is None:
    #     print "20120601 cbss2civilstate None for ", repr(value)
    return str(v)


def cbss2country(code):
    Country = rt.models.countries.Country
    try:
        return Country.objects.get(inscode=code)
    except Country.DoesNotExist:
        dd.logger.warning("Unknown country code %s", code)


def cbss2address(obj, **data):
    n = obj.childAtPath('/Basic/DiplomaticPost')
    if n is not None:
        data.update(
            country=cbss2country(nodetext(n.childAtPath('/CountryCode'))))
        # n.childAtPath('/Post')
        data.update(address=nodetext(n.childAtPath('/AddressPlainText')))
        return data
    n = obj.childAtPath('/Basic/Address')
    if n is not None:
        data.update(
            country=cbss2country(nodetext(n.childAtPath('/CountryCode'))))
        # country = countries.Country.objects.get(
            # inscode=n.childAtPath('/CountryCode').text)
        addr = ''
        # addr += n.childAtPath('/MunicipalityCode').text
        addr += join_words(
            nodetext(n.childAtPath('/Street')),
            nodetext(n.childAtPath('/HouseNumber')),
            nodetext(n.childAtPath('/Box'))
        )
        addr += ', ' + join_words(
            nodetext(n.childAtPath('/PostalCode')),
            nodetext(n.childAtPath('/Municipality'))
        )
        data.update(address=addr)
    return data


