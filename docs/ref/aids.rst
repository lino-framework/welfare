===========
Social aids
===========

..  Building this document requires the lino_welfare.projects.std
    database to be populated.

.. module:: welfare.aids

The :mod:`lino_welfare.modlib.aids` package provides data definitions
for managing "social aids". An "aid" here means the decision that some
client gets some kind of aid during a given lapse of time.

.. contents:: 
   :local:
   :depth: 3


Choicelists
===========

.. class:: AidRegimes

  (Currently not used)

.. class:: ConfirmationTypes

A list of the models that may be used as confirmation.
:ref:`welfare` knows the following confirmation types:

.. django2rst::

  rt.show(aids.ConfirmationTypes)


Models
======

.. class:: AidType

  The type of aid being granted by a granting.
  Every granting has a mandatory pointer (:attr:`Granting.aid_type`) to this.

  .. attribute:: name

    The multilingual name of this aid type.

  .. attribute:: is_urgent

    Whether aid grantings of this type are considered as urgent.
    This is used by :meth:`Confirmation.get_urgent_granting`

  .. attribute:: is_integ_duty

  .. attribute:: short_name

    The short name for internal use.

  .. attribute:: excerpt_title

    The text to print as title in confirmations.

  .. attribute:: board

    Pointer to the default :class:`ml.boards.Board` for aid projects of
    this type.

  .. attribute:: excerpt_type

  .. attribute:: confirmation_type

    Pointer to :class:`ConfirmationTypes`.

  .. attribute:: pharmacy_type

    A pointer to the :class:`welfare.pcsw.ClientContactType` to be
    used when selecting the pharmacy of a refund confirmation 
    (:class:`RefundConfirmation.pharmacy`).

.. class:: Confirmable

  .. attribute:: signer

    The agent who has signed or is expected to sign this item.

.. class:: Granting(Confirmable)

  .. attribute:: aid_type

    The type of aid being granted. Mandatory.
    Pointer to :class:`AidType`.

.. class:: Confirmation(Confirmable)

  .. method:: get_urgent_granting()

    Return the one and only one urgent aid granting for the client and
    period defined for this confirmation.  Return None if there is no
    such granting, or if there is more than one such granting.

.. class:: SimpleConfirmation

.. class:: IncomeConfirmation

.. class:: RefundConfirmation

  .. attribute:: pharmacy

  The pharmacy for which this confirmation is being issued.

  The selection list will work only if the aid type defined on the
  granting of this confirmation has a pharmacy_type defined.

  .. attribute:: doctor
  .. attribute:: doctor_type

.. class:: Category

.. class:: Aid

  .. attribute:: board

  Pointer to the :class:`ml.boards.Board` which decided to allocate
  this aid project.


.. class:: Helper


Tables and Layouts
==================

.. class:: AidsByClient


Templates
=========

Here is a list of the templates defined in the `Aids` module.

.. django2rst::

  try:
    from django.utils import translation
    from atelier.rstgen import header
    from lino.runtime import *

    def f(name):
        print("\n\n.. xfile:: %s\n\n" % name)
    
        print("\nSee the :welfare_srcref:`source code <lino_welfare/modlib/aids/config/aids/Confirmation/%s>`" % name)

        try:
            at = aids.AidType.objects.get(body_template=name)
        except (aids.AidType.MultipleObjectsReturned, aids.AidType.DoesNotExist):
            print("(no example documents)")
            return
    
        qs = at.confirmation_type.model.objects.all()
        qs = qs.filter(granting__aid_type=at, printed_by__isnull=False)
        print("or %d example documents:" % qs.count())

        items = []
        for conf in qs:
            ex = conf.printed_by
            url = "http://de.welfare.lino-framework.org/dl/excerpts/" 
            url += ex.filename_root()
            url += ex.get_build_method().target_ext
            items.append("`%s <%s>`__" % (conf, url))
        print(', '.join(items))

    for name in """
    certificate.body.html
    clothing_bank.body.html
    fixed_income.body.html
    food_bank.body.html
    foreigner_income.body.html
    furniture.body.html
    heating_refund.body.html
    integ_income.body.html
    medical_refund.body.html
    urgent_medical_care.body.html
    """.split():
        if not name.startswith("#"):
            f(name)
    

  except Exception as e:
    print("Oops: %s" % e)

