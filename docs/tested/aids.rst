.. _welfare.tested.aids:

=========================
Social aids (tested tour)
=========================

This document is a technical tour into the
:mod:`lino_welfare.modlib.aids` module.

..  To test only this document:

    $ python setup.py test -s tests.DocsTests.test_aids

    doctest initialization:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.eupen.settings.doctests'
    >>> from lino.api.doctest import *

    >>> ses = rt.login('rolf')
    >>> translation.activate('de')

.. contents::
   :local:
   :depth: 2


ConfirmationTypes
=================

:class:`ConfirmationTypes
<lino_welfare.modlib.aids.choicelists.ConfirmationTypes>` is a
choicelist where each subclass of :class:`Confirmation
<lino_welfare.modlib.aids.mixins.Confirmation>`
has been registered. 

Currently Lino Welfare knows three confirmation types.

>>> ses.show(aids.ConfirmationTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
====== ========================= =================================================== =============
 name   Wert                      Text                                                Vorlage
------ ------------------------- --------------------------------------------------- -------------
        aids.SimpleConfirmation   Einfache Bescheinigung (aids.SimpleConfirmation)    Default.odt
        aids.IncomeConfirmation   Einkommensbescheinigung (aids.IncomeConfirmation)   Default.odt
        aids.RefundConfirmation   Kostenübernahmeschein (aids.RefundConfirmation)     Default.odt
====== ========================= =================================================== =============
<BLANKLINE>


Aid types
==========

This list can be modified by a user with admin level.

>>> ses.show(aids.AidTypes, column_names="name confirmed_by_primary_coach body_template")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
================================================= =========================== ===============================
 Bezeichnung                                       Primärbegleiter bestätigt   Textkörper-Vorlage
------------------------------------------------- --------------------------- -------------------------------
 Ausländerbeihilfe                                 Ja                          foreigner_income.body.html
 Dringende Medizinische Hilfe                      Ja                          urgent_medical_care.body.html
 Eingliederungseinkommen                           Ja                          integ_income.body.html
 Erstattung                                        Ja                          certificate.body.html
 Feste Beihilfe                                    Ja                          fixed_income.body.html
 Heizkosten                                        Ja                          heating_refund.body.html
 Kleiderkammer                                     Ja                          clothing_bank.body.html
 Lebensmittelbank                                  Nein                        food_bank.body.html
 Möbellager                                        Ja                          furniture.body.html
 Übernahme von Arzt- und/oder Medikamentenkosten   Ja                          medical_refund.body.html
 Übernahmeschein                                   Ja                          certificate.body.html
 **Total (11 Zeilen)**                             **10**
================================================= =========================== ===============================
<BLANKLINE>


Hilfebeschlüsse
===============

Alicia hat 2 Hilfebeschlüsse zu bestätigen. Dies kriegt sie als
Willkommensmeldung unter die Nase gerieben:

>>> ses = rt.login('alicia')
>>> translation.activate('de')
>>> for msg in settings.SITE.get_welcome_messages(ses):
...     print(E.tostring(msg))
<span>Du bist besch&#228;ftigt in <em>Beratung mit COLLARD Charlotte (118)</em> (<b>Versammlung beenden</b>). </span>
<span>Du hast 6 Eintr&#228;ge in <b>Zu best&#228;tigende Hilfebeschl&#252;sse</b>.</span>
<b>Du hast 3 offene Datenkontrollen.</b>

When she clicks the link "Zu bestätigende Hilfebeschlüsse", then they show up:

>>> ses.show(aids.MyPendingGrantings)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
======================== ========================= ============== ========== ======= ================================
 Klient                   Hilfeart                  Laufzeit von   bis        Autor   Arbeitsablauf
------------------------ ------------------------- -------------- ---------- ------- --------------------------------
 DUBOIS Robin (179)       Eingliederungseinkommen   23.07.14                          **Unbestätigt** → [Bestätigen]
 DUBOIS Robin (179)       Ausländerbeihilfe         22.06.14                          **Unbestätigt** → [Bestätigen]
 EMONTS-GAST Erna (152)   Heizkosten                30.05.14       31.05.14           **Unbestätigt** → [Bestätigen]
 DA VINCI David (165)     Eingliederungseinkommen   23.05.14                          **Unbestätigt** → [Bestätigen]
 DUBOIS Robin (179)       Eingliederungseinkommen   26.02.13                          **Unbestätigt** → [Bestätigen]
 DA VINCI David (165)     Ausländerbeihilfe         27.01.13                          **Unbestätigt** → [Bestätigen]
======================== ========================= ============== ========== ======= ================================
<BLANKLINE>


Hilfebestätigungen
==================

In der Demo-Datenbank gibt es 2 generierte Bescheinigungen pro Hilfeart :

>>> translation.activate('de')
>>> for at in aids.AidType.objects.exclude(confirmation_type='').order_by('id'):
...    M = at.confirmation_type.model
...    qs = M.objects.filter(granting__aid_type=at)
...    obj = qs[0]
...    txt = obj.confirmation_text()
...    txt = ' '.join(txt.split())
...    print("%s : %d" % (unicode(at), qs.count()))
Eingliederungseinkommen : 20
Ausländerbeihilfe : 35
Feste Beihilfe : 3
Erstattung : 3
Übernahmeschein : 3
Übernahme von Arzt- und/oder Medikamentenkosten : 6
Dringende Medizinische Hilfe : 6
Möbellager : 3
Heizkosten : 3
Lebensmittelbank : 3
Kleiderkammer : 4


Grantings by ISIP contract
==========================

The :meth:`get_aid_type<welfare.isip.ContractBase.get_aid_type>`
method of a contract (called from the `.odt` document template when
printing a :mod:`welfare.isip.Contract` in Eupen) works only when
:meth:`get_granting <welfare.isip.ContractBase.get_granting>` returns
exactly one granting.  Which is the normal situation.

The demo fixtures generate some exceptions to this general rule.  Here
we see that most contracts have indeed exactly 1 granting:

>>> isip.Contract.objects.all().count()
33

>>> l = []
>>> for con in isip.Contract.objects.all():
...     if con.get_aid_type() is not None:
...         l.append(con.id)
>>> print(l)
[1, 3, 4, 7, 9, 10, 11, 12, 14, 17, 18, 19, 22, 24, 27, 29, 32]

>>> rr = aids.IncomeConfirmationsByGranting.insert_action.action.required_roles
>>> print rt.login("rolf").get_user().profile.has_required_roles(rr)
True

>>> ct = contenttypes.ContentType.objects.get_for_model(aids.Granting)
>>> mt = ct.pk
>>> mk = 3

>>> ct = contenttypes.ContentType.objects.get(pk=mt)
>>> ct.model_class()
<class 'lino_welfare.modlib.aids.models.Granting'>


>>> obj = aids.Granting.objects.get(pk=mk)
>>> obj
Granting #3 (u'EiEi/09.10.12/124')

This granting has been confirmed once:

>>> rt.show(aids.IncomeConfirmationsByGranting, obj)
==== ============================ ================ ============ ============= =====
 ID   Klient                       Kategorie        Betrag       Periode vom   bis
---- ---------------------------- ---------------- ------------ ------------- -----
 4    DOBBELSTEIN Dorothée (124)   Zusammenlebend   456,00       09.10.12
                                                    **456,00**
==== ============================ ================ ============ ============= =====
<BLANKLINE>

Permissions
===========

We test whether Theresia is allowed to create an income confirmation.

>>> theresia = rt.login('theresia').user
>>> headers = dict(HTTP_X_REQUESTED_WITH='XMLHttpRequest')
>>> headers.update(REMOTE_USER='rolf')
>>> url = "/api/aids/IncomeConfirmationsByGranting"
>>> url += "?su={2}&mt={0}&mk={1}&an=insert".format(mt, mk, theresia.pk)
>>> res = test_client.get(url, **headers)
>>> print(res.status_code)
200


>>> soup = BeautifulSoup(res.content)
>>> scripts = soup.head.find_all('script', type="text/javascript")

The page header includes a lot of scripts:

>>> len(scripts)
21

Here are the default values for their source URLs:

>>> for s in scripts:
...     print(s.get('src', '(inline)'))
/static/ext-3.3.1/adapter/ext/ext-base-debug.js
/static/ext-3.3.1/ext-all-debug.js
/static/ext-3.3.1/src/locale/ext-lang-de.js
/static/ext-3.3.1/examples/ux/statusbar/StatusBar.js
/static/extjs/Ext.ux.form.DateTime.js
/static/extensible-1.0.1/extensible-all-debug.js
/static/extensible-1.0.1/src/locale/extensible-lang-de.js
/static/tinymce-3.5.11/tiny_mce.js
/static/byteforce/Ext.ux.TinyMCE.js
/static/ext-3.3.1/examples/ux/gridfilters/menu/RangeMenu.js
/static/ext-3.3.1/examples/ux/gridfilters/menu/ListMenu.js
/static/ext-3.3.1/examples/ux/gridfilters/GridFilters.js
/static/ext-3.3.1/examples/ux/gridfilters/filter/Filter.js
/static/ext-3.3.1/examples/ux/gridfilters/filter/StringFilter.js
/static/ext-3.3.1/examples/ux/gridfilters/filter/DateFilter.js
/static/ext-3.3.1/examples/ux/gridfilters/filter/ListFilter.js
/static/ext-3.3.1/examples/ux/gridfilters/filter/NumericFilter.js
/static/ext-3.3.1/examples/ux/gridfilters/filter/BooleanFilter.js
/static/ext-3.3.1/examples/ux/fileuploadfield/FileUploadField.js
/media/cache/js/lino_210_de.js
(inline)


We are interested in the last one, which defines the `onReady` function:

>>> on_ready = unicode(scripts[-1])
>>> len(on_ready.splitlines())
13

And one of these lines calls the Javascript version of the insert
action of :class:`IncomeConfirmationsByGranting
<lino_welfare.modlib.aids.models.IncomeConfirmationsByGranting>`:

>>> "Lino.aids.IncomeConfirmationsByGranting.insert.run" in on_ready
True


The pharmacy of a RefundConfirmation
====================================

The demo database has exactly one AidType with a nonempty
`pharmacy_type` field:

>>> at = aids.AidType.objects.get(pharmacy_type__isnull=False)
>>> at
AidType #6 (u'\xdcbernahme von Arzt- und/oder Medikamentenkosten')


There are 4 pharmacies altogether:

>>> rt.show(pcsw.PartnersByClientContactType, at.pharmacy_type)
=================================== ===== ===============================================
 Name                                ID    Ansicht als
----------------------------------- ----- -----------------------------------------------
 Apotheke Reul                       208   Haushalt, **Partner**, Person, *Organisation*
 Apotheke Schunck                    209   Haushalt, **Partner**, Person, *Organisation*
 Bosten-Bocken A                     211   Haushalt, **Partner**, Person, *Organisation*
 Pharmacies Populaires de Verviers   210   Haushalt, **Partner**, Person, *Organisation*
=================================== ===== ===============================================
<BLANKLINE>


There are two grantings with this aid type:

>>> rt.show(aids.GrantingsByType, at)
==================== ==================== ============== ========== ====
 Beschreibung         Klient               Laufzeit von   bis        ID
-------------------- -------------------- -------------- ---------- ----
 *AMK/27.05.14/139*   JONAS Josef (139)    27.05.14       26.06.14   44
 *AMK/27.05.14/141*   KAIVERS Karl (141)   27.05.14       27.05.14   45
==================== ==================== ============== ========== ====
<BLANKLINE>

Usually there is at most one pharmacy among the client's client
contacts:

>>> rt.show(pcsw.ContactsByClient, pcsw.Client.objects.get(id=139))
==================== =============== =================== =============
 Klientenkontaktart   Organisation    Kontaktperson       Bemerkungen
-------------------- --------------- ------------------- -------------
 Apotheke             Apotheke Reul
 Arzt                                 Waltraud WALDMANN
 Hausarzt                             Werner WEHNICHT
 Zahnarzt                             Dr. Carmen CASTOU
==================== =============== =================== =============
<BLANKLINE>


There is only one pharmacy per client, but in a confirmation I can
manually choose any other pharmacy:

>>> ContentType = rt.modules.contenttypes.ContentType
>>> mt = ContentType.objects.get_for_model(rt.modules.aids.Granting).id
>>> obj = rt.modules.aids.Granting.objects.get(id=44)
>>> url = '/choices/aids/RefundConfirmationsByGranting/pharmacy?mt={0}&mk={1}'.format(mt, obj.id)
>>> response = test_client.get(url, REMOTE_USER="rolf")
>>> result = json.loads(response.content)
>>> for r in result['rows']:
...     print r['text']
<br/>
Apotheke Reul
Apotheke Schunck
Pharmacies Populaires de Verviers
Bosten-Bocken A


Refund confirmations
====================

>>> column_names = "id granting "
>>> column_names += "granting__client "
>>> column_names += "pharmacy doctor_type doctor"
>>> rt.show(aids.RefundConfirmations, column_names=column_names)
==== ================== ====================== ================== ================ =====================
 ID   Hilfebeschluss     Klient                 Apotheke           Art des Arztes   Arzt
---- ------------------ ---------------------- ------------------ ---------------- ---------------------
 12   DMH/28.05.14/144   LAZARUS Line (144)                        Kinderarzt       Dr. Killian KIMMEL
 11   DMH/28.05.14/144   LAZARUS Line (144)                        Zahnarzt         Dr. Carmen CASTOU
 10   DMH/28.05.14/144   LAZARUS Line (144)                        Hausarzt         Werner WEHNICHT
 9    DMH/28.05.14/142   LAMBERTZ Guido (142)                      Arzt             Waltraud WALDMANN
 8    DMH/28.05.14/142   LAMBERTZ Guido (142)                      Kinderarzt       Dr. Killian KIMMEL
 7    DMH/28.05.14/142   LAMBERTZ Guido (142)                      Zahnarzt         Dr. Walter WALDMANN
 6    AMK/27.05.14/141   KAIVERS Karl (141)                        Hausarzt         Werner WEHNICHT
 5    AMK/27.05.14/141   KAIVERS Karl (141)                        Arzt             Waltraud WALDMANN
 4    AMK/27.05.14/141   KAIVERS Karl (141)     Apotheke Schunck   Kinderarzt       Dr. Killian KIMMEL
 3    AMK/27.05.14/139   JONAS Josef (139)                         Zahnarzt         Dr. Carmen CASTOU
 2    AMK/27.05.14/139   JONAS Josef (139)                         Hausarzt         Werner WEHNICHT
 1    AMK/27.05.14/139   JONAS Josef (139)      Apotheke Reul      Arzt             Waltraud WALDMANN
==== ================== ====================== ================== ================ =====================
<BLANKLINE>



Creating a doctor
=================

Here we try to insert a `RefundConfirmation`, specifying a new doctor
in the `doctor` combobox, and leaving the doctor_type empty.

>>> url = "/api/aids/RefundConfirmationsByGranting"
>>> data = dict(
...     mt=119, mk=38,
...     rp="ext-comp-3054",
...     an="submit_insert",
...     start_date="27.05.2014",
...     end_date="27.05.2014",
...     doctor_typeHidden="",
...     doctor_type="Select a Client Contact type...",
...     doctorHidden="Dr. Bean",
...     doctor="Dr. Bean",
...     pharmacyHidden=209,
...     pharmacy="Apotheke Schunck (209)",
...     companyHidden="",
...     company="Select a Organisation...",
...     contact_personHidden='',
...     contact_person="Select a Person...",
...     languageHidden='',
...     language='',
...     remark='')
>>> result = post_json_dict('rolf', url, data)
>>> result.success
False
>>> print(result.message)
Arzt : [u'Kann keinen neuen Arzt erstellen, wenn Art des Arztes leer ist']

Doctor : [u'Cannot auto-create without doctor type']


The period of a confirmation
============================

>>> from lino.utils.format_date import fdl
>>> from lino.mixins.periods import DatePeriod
>>> print(dd.fdl(dd.today()))
22. Mai 2014

We define a utility function:

>>> def f(start_date, end_date):
...     if end_date: end_date = i2d(end_date)
...     if start_date: start_date = i2d(start_date)
...     p = aids.IncomeConfirmation(
...         start_date=start_date, end_date=end_date)
...     for lang in ('en', 'de', 'fr'):
...         translation.activate(lang)
...         print(p.get_period_text())


A **single day**:

>>> f(20140522, 20140522)
on May 22, 2014
am 22. Mai 2014
le 22 mai 2014

A **fully defined** date range:

>>> f(20140522, 20140621)
between May 22, 2014 and June 21, 2014
vom 22. Mai 2014 bis zum 21. Juni 2014
entre le 22 mai 2014 et le 21 juin 2014

The text of a date range **with open end** can differ depending on whether
it is in the future or in the past.

>>> f(20140522, None)
from May 22, 2014
seit dem 22. Mai 2014
depuis le 22 mai 2014

>>> f(20140523, None)
from May 23, 2014
ab dem 23. Mai 2014
à partir du 23 mai 2014


No start date:

>>> f(None, 20140501)
until May 1, 2014
bis zum 1. Mai 2014
jusqu'au 1 mai 2014

Neither start nor end:

>>> f(None, None)
<BLANKLINE>
<BLANKLINE>
<BLANKLINE>
 

