.. _welfare.specs.memo:

==========================
Lino Welfare memo commands
==========================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_memo
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.eupen.settings.demo')
    >>> from lino.api.doctest import *




are rich HTML text
fields which can contain simple HTML formatting like links, tables,
headers, enumerations.

And additionally they can contain :mod:`memo <lino.utils.memo>` markup
commands, i.e. text of the form ``[foo bar baz]``. These memo commands
are going to be "rendered" when this text is being displayed at
certain places.

Examples:

.. _memo.url:

url
===

Insert a link to an external web page. The first argument is the URL
(mandatory). If no other argument is given, the URL is used as
text. Otherwise the remaining text is used as the link text.

The link will always open in a new window (``target="_blank"``)

Usage examples:

- ``[url http://www.example.com]``
- ``[url http://www.example.com example]``
- ``[url http://www.example.com another example]``

..  test:
    >>> ses = rt.login()
    >>> print(ses.parse_memo("See [url http://www.example.com]."))
    See <a href="http://www.example.com" target="_blank">http://www.example.com</a>.
    >>> print(ses.parse_memo("See [url http://www.example.com example]."))
    See <a href="http://www.example.com" target="_blank">example</a>.
    
    >>> print(ses.parse_memo("""See [url https://www.example.com
    ... another example]."""))
    See <a href="https://www.example.com" target="_blank">another example</a>.

    A possible situation is that you forgot the space:
    
    >>> print(ses.parse_memo("See [urlhttp://www.example.com]."))
    See [urlhttp://www.example.com].

    A pitfall is when your editor inserted a non-breaking space:
    
    >>> print(ses.parse_memo("See [url&nbsp;http://www.example.com example]."))
    See <a href="&nbsp;http://www.example.com" target="_blank">example</a>.
    

.. _memo.note:

note
======

Refer to a ticket. Usage example: 

  See ``[note 1]``.

Note that the current renderer decides how to render the link. For
example, the default user interface :mod:`lino.modlib.extjs` (or
:mod:`lino_extjs6.extjs6`, depending on our :attr:`default_ui
<lino.core.site.Site.default_ui>` setting) will render it like this:

>>> ses = rt.login('robin',
...     renderer=settings.SITE.kernel.default_ui.renderer)
>>> print(ses.parse_memo("See [note 1]."))
See <a href="javascript:Lino.notes.Notes.detail.run(null,{ &quot;record_id&quot;: 1 })">#1</a>.

While the plain text renderer will render:

>>> ses = rt.login()
>>> print(ses.parse_memo("See [note 1]."))
See <em>#1</em>.

Referring to a non-existing note:

>>> print(rt.login().parse_memo("See [note 1234]."))
See [ERROR Note matching query does not exist. in '[note 1234]' at position 4-15].


