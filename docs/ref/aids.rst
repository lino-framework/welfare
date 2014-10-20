===========
Social aids
===========

..  Building this document requires the lino_welfare.projects.docs
    database to be populated.

.. module:: welfare

bla

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

.. django2rst::

  rt.show(aids.ConfirmationTypes)


Models
======

.. class:: AidType

  .. attribute:: board

  Pointer to the default :class:`ml.boards.Board` for aid projects of
  this type.

  .. attribute:: excerpt_type

  .. attribute:: confirmation_type

  Pointer to :class:`ConfirmationTypes`.

.. class:: Confirmable

  .. attribute:: signer

  The agent who has signed or is expected to sign this item.

.. class:: Granting(Confirmable)

.. class:: Confirmation(Confirmable)

.. class:: SimpleConfirmation

.. class:: IncomeConfirmation

.. class:: RefundConfirmation

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

Here is a list of the templates defined in this module.

.. django2rst::

  try:
    from django.utils import translation
    from atelier.rstgen import header
    from lino.runtime import *
    # ses = rt.login('hubert')
    # translation.activate('de')

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
    """.split():
        if not name.startswith("#"):
            f(name)
    

  except Exception as e:
    print("Oops: %s" % e)
