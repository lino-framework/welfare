"""Reads the file `FILE.xml` specified as command-line parameter,
replaces all sensitive data by fictive data and writes the result to
`FILE_garbled.xml`.

Typical usage::

  $ python scramble_tx25.py FILE.xml

After running the script, you must still manually:

- verify that no sensitive data has been left ungarbled

- add the garbled file to :mod:`lino_welfare.modlib.cbss.fixtures`
  directory

- modify :mod:`lino_welfare.modlib.cbss.fixtures.cbss_demo` to load
  the new file

After loading the demo database you can test whether your file prints
correctly by issuing::

  $ python manage.py run print_tx25.py ID

Where ID is the primary key of the
:class:`welfare.cbss.RetrieveTIGroupsRequest` that has been created
for your xml file.

"""
from __future__ import print_function
from builtins import range
from builtins import str
from lino import startup
startup('lino_welfare.projects.eupen.settings.demo')

import sys

from collections import namedtuple
from lxml import etree
from lino.utils import Cycler
from lino.api import rt, dd
from lino.utils import demonames

Search = namedtuple('Search', ('expr', 'cycler', 'replacements'))


def main():

    searches = []
    infile = sys.argv[1]
    assert infile.endswith('.xml')
    outfile = infile[:-4] + '_garbled.xml'

    qs = rt.models.pcsw.Client.objects.filter(national_id__isnull=False)
    qs = qs.exclude(birth_date='')
    # print [o.national_id for o in qs]
    CLIENTS = Cycler(qs)

    assert len(CLIENTS)
    
    # first_names = set(demonames.MALE_FIRST_NAMES_FRANCE + demonames.FEMALE_FIRST_NAMES_FRANCE)
    FIRST_NAMES = Cycler(demonames.MALE_FIRST_NAMES_FRANCE,
                         demonames.FEMALE_FIRST_NAMES_FRANCE)
    
    # rt.models.contacts.Person.objects.all().values_list(
    #         'first_name', flat=True))
    # FIRST_NAMES = Cycler(['FIRST_NAME'])
    searches.append(Search("//r:FirstName/r:Label", FIRST_NAMES, dict()))

    # last_names = set(demonames.LAST_NAMES_BELGIUM +
    #                  demonames.LAST_NAMES_MUSLIM + demonames.LAST_NAMES_AFRICAN)
    LAST_NAMES = Cycler(
        demonames.LAST_NAMES_BELGIUM,
        demonames.LAST_NAMES_MUSLIM, demonames.LAST_NAMES_AFRICAN)
    # LAST_NAMES = Cycler(
    #     rt.models.contacts.Person.objects.all().values_list(
    #         'last_name', flat=True))
    # LAST_NAMES = Cycler(['LAST_NAME'])

    CARD_NUMBERS = Cycler([
        '595488123456', '427003123456', '427003123455', '427003123454',
        '427003123453', '427003123452', '427003123451'])
    
    PASSPORT_NUMBERS = Cycler([
        'AE 123456', 'AE 234567', 'AE 345678', 'AE 456789', 'AE 567890'])
    HOUSE_NUMBERS = Cycler([str(i) for i in range(12, 123)])

    searches.append(Search("//r:LastName/r:Label", LAST_NAMES, dict()))
    searches.append(Search("//r:LastName/r:Label", LAST_NAMES, dict()))
    searches.append(Search("//r:CardNumber", CARD_NUMBERS, dict()))
    searches.append(Search("//r:PassportNumber", PASSPORT_NUMBERS, dict()))
    searches.append(Search("//r:Address/r:HouseNumber", HOUSE_NUMBERS, dict()))

    tree = etree.parse(infile)

    changes = 0

    ns = dict(
        soapenv="http://schemas.xmlsoap.org/soap/envelope/",
        r="http://www.ibz.rrn.fgov.be/XSD/xm25/rn25Schema")
    # for expr in ("/soapenv:Envelope", "//r:FirstName/r:Label"):
    #     res = tree.xpath(expr, namespaces=ns)
    #     print expr, len(res)
    # sys.exit(-1)

    NNREP = dict()  # NationalNumber replacements

    for nn in tree.xpath("//r:NationalNumber/r:NationalNumber", namespaces=ns):
        if nn.text and nn.text.strip():
            date = None
            sex = None
            for e in (nn, nn.getparent()):
                dates = e.xpath('r:Date', namespaces=ns)
                if len(dates) == 1:
                    date = dates[0]
                    sexes = e.xpath('r:Sex', namespaces=ns)
                    sex = sexes[0]
            if date is None:
                print(nn.text, "(no date in", nn.tostring())
            else:
                if nn.text not in NNREP:
                    NNREP[nn.text] = CLIENTS.pop()
                obj = NNREP[nn.text]
                if not obj.national_id:
                    raise Exception("%s has no national_id", obj)
                nn.text = obj.national_id
                century, year, month, day = [n.text for n in date]
                print(nn.text, sex.text, century, year, month, day, repr(obj.birth_date))
                bd = obj.birth_date.as_date()
                date[0].text = str(bd.year)[:2]
                date[1].text = str(bd.year)[2:]
                date[2].text = str(bd.month)
                date[3].text = str(bd.day)
                if obj.gender == dd.Genders.male:
                    sex.text = '1'
                elif obj.gender == dd.Genders.female:
                    sex.text = '2'
                changes += 1

    for search in searches:
        for e in tree.xpath(search.expr, namespaces=ns):
            changes += 1
            if not e.text in search.replacements:
                search.replacements[e.text] = search.cycler.pop()
            e.text = search.replacements[e.text]

    # for e in tree.xpath(
    #         "//r:FirstName/r:Label",
    #         namespaces=ns):
    #     changes += 1
    #     obj = CLIENTS.pop()
    #     e.text = obj.first_name

    # for e in tree.getroot().getiterator():
    #     obj = PERSONS.pop()
    #     if e.tag.endswith("}NationalNumber"):
    #         e.text = obj.national_id
    #     if e.tag.endswith("}Nm"):
    #         e.text = PARTNERS.pop().name

    if changes == 0:
        print("No changes.")
        sys.exit(-1)

    for search in searches:
        rep = u", ".join([
            u"{0} -> {1}".format(*i) for i in search.replacements.items()])
        print(u"{0} : {2} ({1} replacements)".format(
            search.expr, len(search.replacements), rep))

    print("Writing {0} changes to {1} ...".format(changes, outfile))
    f = open(outfile, 'wt')
    f.write(etree.tostring(tree, encoding="UTF-8"))
    f.close()

if __name__ == '__main__':
    main()
