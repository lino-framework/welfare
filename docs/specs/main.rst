.. _welfare.tested.main:

===================
The admin main page
===================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_main
    
    doctest init:
    
    >>> from __future__ import print_function
    >>> from lino import startup
    >>> startup('lino_welfare.projects.std.settings.doctests')
    >>> from lino.api.doctest import *
    >>> from lino.utils.html2text import html2text


A technical tour into the :mod:`lino_welfare.modlib.main` module.

.. contents::
   :depth: 2


Test the content of the admin main page.

>>> res = test_client.get('/api/main_html', REMOTE_USER='rolf')
>>> print(res.status_code)
200
>>> result = json.loads(res.content)
>>> result['success']
True
>>> # print(html2text(result['html']))
>>> soup = BeautifulSoup(result['html'])
>>> print(soup.get_text(' ', strip=True))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_CDIFF +SKIP

>>> links = soup.find_all('a')
>>> len(links)
134

>>> print(links[0].text)
Kalender

>>> tables = soup.find_all('table')
>>> len(tables)
5

>>> for h in soup.find_all('h2'):
...     print(h.text.strip())
Benutzer und ihre Klienten
Meine Warteschlange
Meine Termine
Meine Aufgaben
Wartende Besucher


